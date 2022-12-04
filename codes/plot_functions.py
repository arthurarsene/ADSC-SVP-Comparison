import matplotlib.path                 as mpath
import cartopy.crs                     as ccrs
import cartopy.mpl.ticker              as ctk
import cartopy.feature                 as cfeat
import matplotlib.pyplot as plt

def createFigurewithProjection(figsize, nrows, ncols, bounds):
    
    lon_min, lon_max, lat_min, lat_max = bounds
    
    rect = mpath.Path([[lon_min, lat_min], [lon_max, lat_min],
    [lon_max, lat_max], [lon_min, lat_max], [lon_min, lat_min]]).interpolated(50)

    proj=ccrs.NearsidePerspective(central_longitude=(lon_min+lon_max)*0.5,
    central_latitude=(lat_min+lat_max)*0.5)
    
    fig, axes = plt.subplots(nrows=nrows, ncols=ncols, constrained_layout=True, figsize=figsize, subplot_kw={'projection': proj}, dpi=300)
                        
    return fig, axes, rect

def shapeAxis(ax, rect, addCoastline):
    
    proj_to_data = ccrs.PlateCarree()._as_mpl_transform(ax) - ax.transData
    rect_in_target = proj_to_data.transform_path(rect)
    ax.set_boundary(rect_in_target)
    ax.set_xlim(rect_in_target.vertices[:,0].min(), rect_in_target.vertices[:,0].max())
    ax.set_ylim(rect_in_target.vertices[:,1].min(), rect_in_target.vertices[:,1].max())
    
    if addCoastline:
        ax.coastlines(zorder=3, linewidth=2)
        ax.add_feature(cfeat.LAND, color='lightgrey', zorder=3)

    gl=ax.gridlines(draw_labels=True, x_inline=False, y_inline=False, linestyle='dashed')
    gl.top_labels=False
    gl.right_labels=False
    gl.rotate_labels=False
    gl.xlocator=ctk.LongitudeLocator(4)
    gl.ylocator=ctk.LatitudeLocator(6)
    gl.xformatter=ctk.LongitudeFormatter(zero_direction_label=True)
    gl.yformatter=ctk.LatitudeFormatter()
    gl.xlabel_style = {'size': 14}
    gl.ylabel_style = {'size': 14}
# Import libraries

import matplotlib.path                 as mpath
import cartopy.crs                     as ccrs
import cartopy.mpl.ticker              as ctk
import cartopy.feature                 as cfeat
import matplotlib.pyplot as plt
import numpy as np


# Import data

iso600 = np.loadtxt('../data/bathy/smooth_600m_isobath.txt')
x600 = iso600[:,0]
y600 = iso600[:,1]

iso000 = np.loadtxt('../data/bathy/smooth_0m_isobath.txt')
x000 = iso000[:,0]
y000 = iso000[:,1]


# Define functions

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

def AlongAcrossComponent(lon, lat, comp):
    
    ALONG = []
    ACROSS = []
    
    for i in range(len(lon)):
        lonsel = lon[i]
        latsel = lat[i]
        complex_velocity = comp[i]

        # Closest point on the shelfbreak
        az12, az21, dist = g.inv(np.ones(len(x600))*lonsel, np.ones(len(x600))*latsel, x600, y600)
        dist_clos = dist[np.argmin(dist)]
        az_clos = az12[np.argmin(dist)]
        x_clos = np.sin(np.deg2rad(az_clos))*dist_clos
        y_clos = np.cos(np.deg2rad(az_clos))*dist_clos
        z_clos = x_clos + 1j*y_clos
        xshel, yshel = x600[np.argmin(dist)], y600[np.argmin(dist)]

        # Closest point on the coast
        az12, az21, dist = g.inv(np.ones(len(x000))*lonsel, np.ones(len(x000))*latsel, x000, y000)
        dist_coast = dist[np.argmin(dist)]
        xcoas, ycoas = x000[np.argmin(dist)], y000[np.argmin(dist)]

        width_shelf = g.inv(xcoas, ycoas, xshel, yshel)[2]

        # Compute velocities
        angles = np.abs(np.angle(z_clos/complex_velocity))

        dist_along = np.sin(angles)*np.abs(complex_velocity)
        dist_across = np.cos(angles)*np.abs(complex_velocity)

        angles = np.angle(z_clos/complex_velocity)
        vel_along = np.sin(angles)*np.abs(complex_velocity)
        vel_across = np.cos(angles)*np.abs(complex_velocity)

        if (dist_coast>dist_clos)&(dist_coast>width_shelf):

            vel_along*=-1
            vel_across*=-1
        
        ALONG.append(vel_along)
        ACROSS.append(vel_across)


    return np.array(ALONG), np.array(ACROSS)


def CenterGravity(lons, lats):
    
    lats = np.deg2rad(lats)
    lons = np.deg2rad(lons)

    X = np.cos(lats) * np.cos(lons)
    Y = np.cos(lats) * np.sin(lons)
    Z = np.sin(lats)

    x = np.mean(X)
    y = np.mean(Y)
    z = np.mean(Z)

    Lon = np.arctan2(y, x)
    Hyp = np.sqrt(x**2 + y**2)
    Lat = np.arctan2(z, Hyp)
    
    return np.rad2deg([Lon, Lat])


def drifterDailyResampling(timeaxis, drifter_dataset, shift=12):

    lon_origin = drifter_dataset.longitude.values
    lat_origin = drifter_dataset.latitude.values
    time_origin = drifter_dataset.time.values

    time12h_shift = np.unique(timeaxis[:-1]+np.timedelta64(shift, 'h'))
    lon_00 = np.zeros(len(time12h_shift))
    lat_00 = np.zeros(len(time12h_shift))
    dt = float(np.diff(np.unique(timeaxis))[0])*1e-9

    arg = np.array([np.argmin(np.abs(time_origin[i] - time12h_shift)) for i in range(len(time_origin))])

    for d in range(len(time12h_shift)):
        lons = lon_origin[arg==d]
        lats = lat_origin[arg==d]
        lo, la = CenterGravity(lons[(~np.isnan(lons))&(~np.isnan(lats))], lats[(~np.isnan(lons))&(~np.isnan(lats))])
        lon_00[d] = lo
        lat_00[d] = la

    notnan = (~np.isnan(lon_00))
    lon_00 = lon_00[notnan]
    lat_00 = lat_00[notnan]
    time_00 = time12h_shift[notnan]

    #Compute velocity with centered scheme (for indx 1 to -2)
    dazim,az21,dist = g.inv(lon_00[:-1],lat_00[:-1],lon_00[1:],lat_00[1:])
    dvelo = dist/(dt)
    U = np.sin(np.deg2rad(dazim))*dvelo
    V = np.cos(np.deg2rad(dazim))*dvelo
    AZ = dazim
    TIME = time_00[:-1]+np.timedelta64(shift, 'h')

    c_grav = np.array([CenterGravity([lon_00[i], lon_00[i+1]] , [lat_00[i], lat_00[i+1]]) for i in range(len(lon_00)-1)])
    LON, LAT = c_grav[:, 0], c_grav[:, 1]
    
    complex_velocity = U + 1j*V
    ALONG, ACROSS = AlongAcrossComponent(LON, LAT, complex_velocity)

    return TIME, LON, LAT, U, V, ALONG, ACROSS
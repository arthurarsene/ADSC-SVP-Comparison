# Import libraries

import matplotlib.path                 as mpath
import cartopy.crs                     as ccrs
import cartopy.mpl.ticker              as ctk
import cartopy.feature                 as cfeat
import matplotlib.pyplot as plt

from matplotlib.projections import PolarAxes
import mpl_toolkits.axisartist.grid_finder as gf
import mpl_toolkits.axisartist.floating_axes as fa

import numpy as np

from pyproj import Geod
g = Geod(ellps='WGS84')



import warnings

# Hide the warnings caused by hidden legend on Taylor diagrams
warnings.simplefilter(action='ignore', category=UserWarning)

# Import data

iso600 = np.loadtxt('../data/bathy/smooth_600m_isobath.txt')
x600 = iso600[:,0]
y600 = iso600[:,1]

iso000 = np.loadtxt('../data/bathy/smooth_0m_isobath.txt')
x000 = iso000[:,0]
y000 = iso000[:,1]


# Define functions

############### PLOTS ############### 

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

# Plot Taylor diagram from Y. Copin's code (10.5281/zenodo.5548061)
class TaylorDiagram(object):
    def __init__(self, STD ,fig=None, rect=111, label='_'):
        self.STD = STD
        tr = PolarAxes.PolarTransform()
        # Correlation labels
        rlocs = np.concatenate(((np.arange(11.0) / 10.0), [0.95, 0.99]))
        tlocs = np.arccos(rlocs) # Conversion to polar angles
        gl1 = gf.FixedLocator(tlocs) # Positions
        tf1 = gf.DictFormatter(dict(zip(tlocs, map(str, rlocs))))
        # Standard deviation axis extent
        self.smin = 0
        self.smax = 1.5 * self.STD
        gh = fa.GridHelperCurveLinear(tr,extremes=(0,(np.pi/2),self.smin,self.smax),grid_locator1=gl1,tick_formatter1=tf1,)
        if fig is None:
            fig = plt.figure()
        ax = fa.FloatingSubplot(fig, rect, grid_helper=gh)
        fig.add_subplot(ax)
        # Angle axis
        ax.axis['top'].set_axis_direction('bottom')
        ax.axis['top'].label.set_text("CORRELATION COEFFICIENT $R$")
        ax.axis['top'].label.set_fontsize(15)
        ax.axis['top'].toggle(ticklabels=True, label=True)
        ax.axis['top'].major_ticklabels.set_axis_direction('top')
        ax.axis['top'].label.set_axis_direction('top')
        # X axis
        ax.axis['left'].set_axis_direction('bottom')
        ax.axis['left'].label.set_text("NORMALIZED STANDARD DEVIATION $\hat{\sigma_f}$")
        ax.axis['left'].label.set_fontsize(15)
        ax.axis['left'].toggle(ticklabels=True, label=True)
        ax.axis['left'].major_ticklabels.set_axis_direction('bottom')
        ax.axis['left'].label.set_axis_direction('bottom')
        # Y axis
        ax.axis['right'].set_axis_direction('top')
        ax.axis['right'].label.set_text("NORMALIZED STANDARD DEVIATION $\hat{\sigma_f}$")
        ax.axis['right'].label.set_fontsize(15)
        ax.axis['right'].toggle(ticklabels=True, label=True)
        ax.axis['right'].major_ticklabels.set_axis_direction('left')
        ax.axis['right'].label.set_axis_direction('top')
        # Useless
        ax.axis['bottom'].set_visible(False)
        # Contours along standard deviations
        ax.grid()
        self._ax = ax # Graphical axes
        self.ax = ax.get_aux_axes(tr) # Polar coordinates
        # Add reference point and STD contour
        l , = self.ax.plot([0], self.STD, color='navy', marker='o', ls='', ms=8)#, label=label)
        t = np.linspace(0, (np.pi / 2.0))
        r = np.zeros_like(t) + self.STD
        self.ax.plot(t, r, color='navy', ls='-', label='_', lw=2)
        # Collect sample points for latter use (e.g. legend)
        self.samplePoints = [l]
    def add_sample(self,STD,r,*args,**kwargs):
        l,= self.ax.plot(np.arccos(r), STD, *args, **kwargs) # (theta, radius)
        self.samplePoints.append(l)
        return l
    def add_contours(self,levels=[0.2, 0.4, 0.6, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95, 1.0],**kwargs):
        possible_std = np.linspace(self.smin, self.smax, 200)
        possible_correl = np.linspace(0, 1, 200)
        mesh_std, mesh_correl = np.meshgrid(possible_std, possible_correl)

        R0 = 1
        tss = (4*(1+mesh_correl))/(((mesh_std+(1/mesh_std))**2) * (1+R0))
        
        contours = self.ax.contour(np.arccos(mesh_correl), mesh_std, tss, levels, **kwargs)
        
        return contours

def srl(obsSTD, s, r, l, boolean, fname, cs, mark, size, alpha, title):
    fig=plt.figure(figsize=(9,9), dpi=300)
    dia=TaylorDiagram(obsSTD, fig=fig, rect=111, label='Reference ${\sigma_r}$')
    plt.clabel(dia.add_contours(colors='0.5'), inline=1, fontsize=14)

    srlc = zip(s, r, l, boolean, cs, mark, size, alpha)
    for i in srlc:
        if i[3]:
            dia.add_sample(i[0], i[1], label=i[2], c=i[4], marker=i[5], markersize=i[6], alpha=i[7])
        else:
            dia.add_sample(i[0], i[1], c=i[4], marker=i[5], markersize=i[6], alpha=i[7])
        spl = [p.get_label() for p in dia.samplePoints]

        fig.legend(dia.samplePoints, spl, numpoints=1, prop=dict(size='12.7'), loc='upper right', bbox_to_anchor=(0.7, 0.4, 0.5, 0.5), framealpha=1)

    plt.title(title, fontsize=16)
    plt.text(obsSTD+0.03, +0.03, 'Reference ${\sigma_r}$', fontsize=15, color='navy')

    plt.tight_layout()


############### COMPUTE ###############

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

    lon_origin = drifter_dataset.lon.values
    lat_origin = drifter_dataset.lat.values
    time_origin = drifter_dataset.time.values

    time12h_shift = np.unique(timeaxis[:-1]+np.timedelta64(shift, 'h'))
    lon_00 = np.zeros(len(time12h_shift))*np.nan
    lat_00 = np.zeros(len(time12h_shift))*np.nan
    dt = float(np.diff(np.unique(timeaxis))[0])*1e-9

    arg = np.array([np.argmin(np.abs(time_origin[i] - time12h_shift)) for i in range(len(time_origin))])

    for d in range(len(time12h_shift)):
        lons = lon_origin[arg==d]
        lats = lat_origin[arg==d]

        if len(lons)>0:
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
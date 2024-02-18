
# electron beam
from shadow4.sources.s4_electron_beam import S4ElectronBeam
electron_beam = S4ElectronBeam(energy_in_GeV=1.9,energy_spread=0,current=0.4)
electron_beam.set_sigmas_all(sigma_x=3.9e-05,sigma_y=3.1e-05,sigma_xp=3.92e-05,sigma_yp=3.92e-05)

# magnetic structure
from shadow4.sources.undulator.s4_undulator import S4Undulator
source = S4Undulator(
    K_vertical        = 0.25, # syned Undulator parameter
    period_length     = 0.032, # syned Undulator parameter
    number_of_periods = 50, # syned Undulator parameter
    emin              = 10500.0, # Photon energy scan from energy (in eV)
    emax              = 10500.0, # Photon energy scan to energy (in eV)
    ng_e              = 1, # Photon energy scan number of points
    maxangle          = 0.015, # Maximum radiation semiaperture in RADIANS
    ng_t              = 100, # Number of points in angle theta
    ng_p              = 11, # Number of points in angle phi
    ng_j              = 20, # Number of points in electron trajectory (per period) for internal calculation only
    code_undul_phot   = 'pysru', # internal, pysru, srw
    flag_emittance    = 1, # when sampling rays: Use emittance (0=No, 1=Yes)
    flag_size         = 2, # when sampling rays: 0=point,1=Gaussian,2=FT(Divergences)
    use_gaussian_approximation = 0, # use Gaussian approximation for generating simplified beam
    distance          = 100.0, # distance to far field plane
    srw_range         = 0.05, # for SRW backpropagation, the range factor
    srw_resolution    = 50, # for SRW backpropagation, the resolution factor
    srw_semianalytical= 0, # for SRW backpropagation, use semianalytical treatement of phase
    magnification     = 0.05, # for internal/wofry backpropagation, the magnification factor
    pysru_source      = 1, # for pysru/wofry backpropagation: source interpolated from polar (0) or recalculated (1)
    )


# light source
from shadow4.sources.undulator.s4_undulator_light_source import S4UndulatorLightSource
light_source = S4UndulatorLightSource(name='undulator', electron_beam=electron_beam, magnetic_structure=source,nrays=500,seed=5676561)
beam = light_source.get_beam()

# test plot
from srxraylib.plot.gol import plot_scatter
rays = beam.get_rays()
plot_scatter(1e6 * rays[:, 0], 1e6 * rays[:, 2], title='(X,Z) in microns')
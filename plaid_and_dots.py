#%%
from psychopy import visual, clock
from psychopy.iohub import client
import percepts
import utils
import stims
import expsetup
import numpy as np


# setting up the plaids
init = utils.load_init('./config/init.yaml') 
# get the stim parameters
stim_params = init['experiment']['stim']
# launch a win instance to intercept the keypresses 
# so that they are not sent to the console
# set-up the Display and monitor
# make a monitor with monitor constants from the init file
mon = expsetup.makeMonitor(init['monitor_constants'])  
# and make a window using that monitor
win = visual.Window(
    monitor=mon, 
    color=init['experiment']['bkgcolor'],
    size=mon.getSizePix(), 
    units='deg', 
    screen=1,  # 0 is the monitor of the experiment control
    fullscr=True, 
    allowGUI=False,  
    waitBlanking=False, 
    allowStencil=True,
    winType='pyglet')  # for iohub to function well

aperture = visual.Aperture(win, size=20)
aperture.units='deg'

# velocity is upward, computed from the oblique velocity vector
# this velocity is in periods/s 
# the velocity is thus relatif to the vertical period which is 1/(sin(theta)*sf) [deg]
vel_ori = -90

sf_x = stims.get_angular_frequency(0, stim_params['sf'], stim_params['ori'])
sf_y = stims.get_angular_frequency(90, stim_params['sf'], stim_params['ori'])
v_y = stims.get_angular_velocity(90, stim_params['vel'], stim_params['ori'])
velocity = lambda vel_ori: np.array([v_y * sf_x * np.cos(stims._deg2rad(vel_ori)),
                                     v_y * sf_y * np.sin(stims._deg2rad(vel_ori))])

# the actual plaids stimulus
# plaid_stims = stims.plaids(win, **stim_params)
plaid = stims.transparent_Plaid(win, **stim_params)
plaid.phase = np.random.uniform(size=(2,))
win.getMovieFrame(buffer='back')


# the superimposed RDK
dots = stims.createDots(
    win,
    stim_params['alpha'], 
    stim_params['dc'],
    nDots=500,
    I0=stim_params['I0'])
dots.coherence = 1
current_dir = None
dots_velocity = lambda x: min(
    stims.get_angular_velocity(x, stim_params['vel'], stim_params['ori']),
    stims.get_angular_velocity(x, stim_params['vel'], -stim_params['ori']))

# the fixation disk
fix_disk = stims.fixation_disk(win)

# Start the ioHub process. 'io' can now be used during the
# experiment to access iohub devices and read iohub device events
io = client.launchHubServer()
io.devices.mouse.reporting = False

msg = 'Press [SPACE] to continue... '
print(msg)
visual.TextStim(win, msg, color=stim_params['I0']).draw()
 
win.flip()
percepts.waitKeyPress(io, key=' ', timeout=5)

all_percepts = []
trial_timer = clock.CountdownTimer(start=30)

pb = percepts.get_percept_report(io, clear=True)
current_percept = pb[-1]

new_time = trial_timer.getTime()

plaid.autoDraw = True


#win.getMovieFrame(buffer='back')
#win.getMovieFrame()


#dots.autoDraw = True
for s in fix_disk: s.autoDraw = True
aperture.enable()

while trial_timer.getTime()>0:
    old_time = new_time
    new_time = trial_timer.getTime()
    
    if new_time > 30:
        dots.dir = 0
        dots.coherence = 0
        vel_ori = -90
    elif new_time > 20:
        dots.coherence = stim_params['coherence']
        dots.dir = -90 - stim_params['ori']  # "left"
        # dots.element.ori = 20
        # vel_ori = 0  # -90 + stim_params['ori']
    elif new_time > 10:
        dots.dir = -90  # "up"
        # dots.element.ori = 90
        vel_ori = -90
    else:
        dots.dir = -90 + stim_params['ori']  # "right"
        # dots.element.ori = 160
        # vel_ori = -180  # -90 - stim_params['ori']q

    if dots.dir != current_dir:
        dots_vel = dots_velocity(dots.dir)
        # print(dots.dir, ': ', dots_vel)
        current_dir = dots.dir

    dots.speed = dots_vel * (new_time - old_time)  # speed in °/frame
    plaid.phase += velocity(vel_ori) * (new_time - old_time)
    win.flip()

    

pb = percepts.get_percept_report(io)
io.devices.keyboard.reporting = False
print('Trial ended')

pb = percepts.merge_percepts(pb)
print(pb)

plaid.autoDraw = False

#dots.autoDraw = False
for s in fix_disk: s.autoDraw = False
aperture.disable()



msg = 'Press [q] to quit... '
print(msg)
visual.TextStim(win, msg, color=stim_params['I0']).draw()
win.flip()
percepts.waitKeyPress(io, key='q', timeout=20)

# %%

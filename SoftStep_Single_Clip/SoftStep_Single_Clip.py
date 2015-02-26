#-----------------------------------------------
#                        
#  Author:  
#    Evan Bogunia evanbeta@keithmcmillen.com                 
#                        
#-----------------------------------------------

from __future__ import with_statement

import Live
import time

from _Framework.ButtonElement import ButtonElement
from _Framework.ChannelStripComponent import ChannelStripComponent
from _Framework.ClipSlotComponent import ClipSlotComponent
from _Framework.CompoundComponent import CompoundComponent
from _Framework.ControlElement import ControlElement
from _Framework.ControlSurface import ControlSurface
from _Framework.ControlSurfaceComponent import ControlSurfaceComponent
from _Framework.InputControlElement import *
from _Framework.MixerComponent import MixerComponent
from _Framework.SceneComponent import SceneComponent
from _Framework.SessionComponent import SessionComponent
from _Framework.SessionZoomingComponent import SessionZoomingComponent
from _Framework.EncoderElement import EncoderElement
from _Framework.ToggleComponent import ToggleComponent
from SoftstepSessionComponent import SoftstepSessionComponent

#define global variables
CHANNEL = 8  #channels are numbered 0 - 15
is_momentary = True

class SoftStep_Single_Clip(ControlSurface):
  __module__ = __name__
  __doc__ = "SoftStep Clip Launching controller script"
  
  def __init__(self, c_instance):
    ControlSurface.__init__(self, c_instance)
    with self.component_guard():
      self._setup_mixer_control()
      self._setup_session_control()
      self._setup_channel_strip_control()
      self.set_highlighting_session_component(self.session)

  def _setup_session_control(self):
    num_tracks = 1 #4 columns (tracks)
    num_scenes = 1 #2 rows (scenes)
    
    #(num_tracks, num_scenes) a session highlight ("red box") will appear with any two non-zero values
    self.session = SoftstepSessionComponent(num_tracks,num_scenes)
    #(track_offset, scene_offset) Sets the initial offset of the "red box" from top left
    self.session.set_offsets(0,0)
    
    self.session.set_select_buttons(ButtonElement(is_momentary,MIDI_CC_TYPE,CHANNEL,74), ButtonElement(is_momentary,MIDI_CC_TYPE,CHANNEL,73))
    self.session.set_scene_bank_buttons(ButtonElement(is_momentary,MIDI_CC_TYPE,CHANNEL,72), ButtonElement(is_momentary,MIDI_CC_TYPE,CHANNEL,71))

    self.session.set_track_bank_buttons(ButtonElement(is_momentary,MIDI_CC_TYPE,CHANNEL,75), ButtonElement(is_momentary,MIDI_CC_TYPE,CHANNEL,76))
    
    self.session.selected_scene().set_launch_button(ButtonElement(is_momentary, MIDI_CC_TYPE, CHANNEL, 114))
    #self.session.set_stop_all_clips_button(ButtonElement(is_momentary, MIDI_CC_TYPE, CHANNEL, 75))

    #here we set up the clip launch assignments for the session  
    clip_launch_notes = [112]
    index = 0
    '''
    for scenes in range(num_scenes):
    	for tracks in range(num_tracks):
      		#step though scenes and assign a note to first slot of each
    		self.session.scene(scenes).clip_slot(tracks).set_started_value(1)
      		self.session.scene(scenes).clip_slot(tracks).set_stopped_value(0)
      		self.session.scene(scenes).clip_slot(tracks).set_launch_button(ButtonElement(is_momentary,MIDI_CC_TYPE,CHANNEL,clip_launch_notes[index]))
      		index += 1
    '''
    self.session.scene(0).clip_slot(0).set_started_value(1)
    self.session.scene(0).clip_slot(0).set_stopped_value(0)
    self.session.scene(0).clip_slot(0).set_launch_button(ButtonElement(is_momentary,MIDI_CC_TYPE,CHANNEL,111))

    #here we set up a mixer and channel strip(s) which move with the session
    self.session.set_mixer(self.mixer)  #bind the mixer to the session so that they move together
    self.session.update()

  def _setup_mixer_control(self):
    #A mixer is one-dimensional; here we define the width in tracks
    num_tracks = 1
    #set up the mixer
    self.mixer = MixerComponent(num_tracks, 2, with_eqs=True, with_filters=True)  #(num_tracks, num_returns, with_eqs, with_filters)
    self.mixer.set_track_offset(0)  #sets start point for mixer strip (offset from left)
    #set the selected strip to the first track, so that we don't assign a button to arm the master track, which would cause an assertion error
    self.song().view.selected_track = self.mixer.channel_strip(0)._track


  def _setup_channel_strip_control(self):
  	self.channelstrip = ChannelStripComponent()
  	self.channelstrip.set_track(self.mixer.channel_strip(0)._track)
  	self.channelstrip.set_arm_button(ButtonElement(is_momentary, MIDI_CC_TYPE, CHANNEL, 112))
  	
  def _on_selected_track_changed(self):
  	self.channelstrip.set_track(self.song().view.selected_track)
  
  def disconnect(self):
    #clean things up on disconnect
    
    #create entry in log file
    self.log_message(time.strftime("%d.%m.%Y %H:%M:%S", time.localtime()) + "----------SoftStep ClipLaunching log closed----------")
    
    ControlSurface.disconnect(self)
    return None

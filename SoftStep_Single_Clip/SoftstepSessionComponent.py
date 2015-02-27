from _Framework.SessionComponent import *


class SoftStepSessionComponent(SessionComponent):
  __module__ = __name__
  """ Custom session component for SoftStep"""

  def __init__(self, num_tracks, num_scenes):
    self._undo_button = None
    SessionComponent.__init__(self, num_tracks, num_scenes)


  """ Adding An Undo Button to the Session Component"""


  def set_undo_button(self, button):
    self._undo_button = button
    self._undo.subject = button
  
  @subject_slot('value')
  def _undo(self, value):
    if value != 0:
      self.song().undo()

  def update(self):
    SessionComponent.update(self)
    self._reselect_track()
    self._reselect_scene()

  """ Because update doesn't get called in Live 9 when we change offsets 
      We have to manually call reselect_track whenever we bank
  """
  def set_offsets(self, track_offset, scene_offset):
    SessionComponent.set_offsets(self, track_offset, scene_offset)
    self._reselect_track()
  
  def _reselect_track(self):
    tracks_to_use = self.tracks_to_use()
    track = tracks_to_use[self._track_offset] 
    self.song().view.selected_track = track
  
  def on_selected_scene_changed(self):
    SessionComponent.on_selected_scene_changed(self)
    self._reselect_scene()
    
  def _reselect_scene(self):
    selected_scene = self.song().view.selected_scene
    all_scenes = self.song().scenes
    sceneIndex = list(all_scenes).index(selected_scene)
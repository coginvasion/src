# Embedded file name: lib.coginvasion.gags.TNT
"""

  Filename: TNT.py
  Created by: DecodedLogic (08Jul15)

"""
from lib.coginvasion.gags.TossTrapGag import TossTrapGag
from lib.coginvasion.gags.GagState import GagState
from lib.coginvasion.gags import GagGlobals
from lib.coginvasion.globals import CIGlobals
from direct.interval.IntervalGlobal import Sequence, Wait, Func
from direct.interval.SoundInterval import SoundInterval
from direct.actor.Actor import Actor

class TNT(TossTrapGag):

    def __init__(self):
        TossTrapGag.__init__(self, CIGlobals.TNT, 'phase_5/models/props/tnt-mod.bam', 180, 'phase_3.5/audio/sfx/ENC_cogfall_apart.mp3', 'phase_5/audio/sfx/TL_dynamite.mp3', particlesFx='phase_5/etc/tnt.ptf', anim='phase_5/models/props/tnt-chan.bam')
        self.maxDistance = GagGlobals.TNT_RANGE
        self.setImage('phase_3.5/maps/tnt.png')

    def start(self):
        super(TNT, self).start()
        self.startTrap()
        if base.localAvatar == self.avatar:
            Sequence(Wait(1.5), Func(base.localAvatar.b_gagRelease, self.getID())).start()

    def release(self):
        super(TNT, self).release()
        self.entity = self.gag
        self.gag = None
        return

    def equip(self):
        self.build()
        super(TNT, self).equip()
        if not self.gag:
            self.build()
            self.gag.reparentTo(self.handJoint)

    def unEquip(self):
        TossTrapGag.unEquip(self)

    def onCollision(self, entry):
        TossTrapGag.onCollision(self, entry)
        base.localAvatar.b_gagCollision(self.getID())
        self.doCollision()

    def doCollision(self):
        if not self.entity:
            self.build()
            self.entity = self.gag
            self.gag = None
        if self.wantParticles:
            if not self.particles:
                self.buildParticles()
            emitter = self.entity.find('**/joint_attachEmitter')
            self.particles.start(parent=emitter, renderParent=emitter)
        base.audio3d.attachSoundToObject(self.idleSfx, self.gag)
        self.idleSfx.play()
        if self.entity and self.anim:
            self.entity.play('chan')
        if self.track:
            self.track.pause()
            self.track = None
        if self.isLocal():
            Sequence(Wait(2), Func(self.avatar.b_gagActivate, self.getID())).start()
        return

    def explode(self):
        self.explosion = Actor('phase_5/models/props/kapow-mod.bam', {'chan': 'phase_5/models/props/kapow-chan.bam'})
        self.explosion.reparentTo(render)
        self.explosion.setBillboardPointEye()
        self.explosion.setPos(self.entity.getPos(render) + (0, 0, 4))
        self.explosion.setScale(0.5)
        self.explosion.play('chan')
        if self.idleSfx:
            self.idleSfx.stop()
        base.audio3d.attachSoundToObject(self.hitSfx, self.explosion)
        SoundInterval(self.hitSfx).start()
        self.cleanupParticles()
        self.cleanupEntity()
        self.setState(GagState.LOADED)
        backpack = self.avatar.getBackpack()
        if backpack.getSupply(self.getName()) > 0 and backpack.getCurrentGag() == self:
            self.equip()
            if hasattr(self.avatar, 'enablePieKeys'):
                self.avatar.enablePieKeys()
        Sequence(Wait(0.5), Func(self.cleanupExplosion)).start()

    def activate(self):
        if not self.entity:
            return
        for obj in base.cr.doId2do.values():
            if obj.__class__.__name__ == 'DistributedSuit':
                if obj.getPlace() == base.localAvatar.zoneId:
                    if obj.getDistance(self.entity) <= self.maxDistance:
                        if self.avatar.doId == base.localAvatar.doId:
                            self.avatar.sendUpdate('suitHitByPie', [obj.doId, self.getID()])

        self.explode()

    def cleanupEntity(self):
        if self.entity:
            self.entity.cleanup()
            self.entity = None
        return

    def cleanupExplosion(self):
        if self.explosion:
            self.explosion.cleanup()
            self.explosion.removeNode()
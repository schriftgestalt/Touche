# encoding: utf-8
from __future__ import division, print_function, unicode_literals

from fontTools.pens.basePen import BasePen
import traceback

class SegmentsPen(BasePen):
    
    def __init__(self, glyphSet, masterID):
        BasePen.__init__(self, glyphSet)
        self.segments = []
        self._masterID = masterID
    
    def addSegment(self, segment):
        self.segments.append(segment)
    
    def _moveTo(self, pt):
        self.previousPoint = pt
        self.firstPoint = pt
    
    def _lineTo(self, pt):
        self.addSegment((self.previousPoint, pt))
        self.previousPoint = pt
    
    def _curveToOne(self, pt1, pt2, pt3):
        self.addSegment((self.previousPoint, pt1, pt2, pt3))
        self.previousPoint = pt3
    
    def closePath(self):
        if self.firstPoint != self.previousPoint:
            self.lineTo(self.firstPoint)
    
    def addComponent(self, glyphName, transformation):
        """This default implementation simply transforms the points
        of the base glyph and draws it onto self.
        """
        from fontTools.pens.transformPen import TransformPen
        try:
            glyph = self.glyphSet[glyphName]
            layer = glyph.layers[self._masterID]
        except KeyError:
            pass
        else:
            tPen = TransformPen(self, transformation)
            layer.draw(tPen)# coding=utf-8

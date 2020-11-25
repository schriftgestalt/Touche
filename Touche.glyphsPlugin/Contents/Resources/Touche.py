# encoding: utf-8
from __future__ import division, print_function, unicode_literals

import SegmentsPen

from GlyphsApp import *

from Foundation import NSBundle, NSOffsetRect, NSIntersectsRect, NSPointInRect, NSMinX, NSMinY, NSMaxX, NSMaxY
import objc
_path = NSBundle.mainBundle().bundlePath()
_path = _path+"/Contents/Frameworks/GlyphsCore.framework/Versions/A/Resources/BridgeSupport/GlyphsCore.bridgesupport"
f = open(_path)
objc.parseBridgeSupport(f.read(), globals(), _path)
f.close()

def segmentInBound(segment, bounds):
    minX = NSMinX(bounds)
    minY = NSMinY(bounds)
    maxX = NSMaxX(bounds)
    maxX = NSMaxY(bounds)
    for point in segment:
        if NSPointInRect(point, bounds):
            return True
        found = minX <= point[0] <= maxX
        if found:
            return True
    return False
    
class Touche(object):
    """Checks a font for touching glyphs.
    
        font = CurrentFont()
        a, b = font['a'], font['b']
        touche = Touche(font)
        touche.checkPair(a, b)
        touche.findTouchingPairs([a, b])
    
    Public methods: checkPair, findTouchingPairs
    """

    def __init__(self, font, masterID):
        self.font = font
        self.penCache = {}
        self._masterID = masterID
        #self.flatKerning = font.naked().flatKerning

    def findTouchingPairs(self, glyphs):
        """Finds all touching pairs in a list of glyphs.

        Returns a list of tuples containing the names of overlapping glyphs
        """
        
        # lookup all sidebearings
        lsb, rsb = ({} for i in range(2))
        for g in glyphs:
            lsb[g], rsb[g] = g.LSB, g.RSB
        self.lsb, self.rsb = lsb, rsb
        
        pairs = [(g1, g2) for g1 in glyphs for g2 in glyphs]
        return [(g1.parent.name, g2.parent.name) for (g1, g2) in pairs if self.checkPair(g1, g2)]

    # def getKerning(self, g1, g2):
    #     return self.flatKerning.get((g1.name, g2.name), 0)

    def checkPair(self, g1, g2):
        """New checking method contributed by Frederik

        Returns a Boolean if overlapping.
        """
        if Glyphs.versionNumber >= 3:
            kern = g1.nextKerningForLayer_direction_(g2, LTR)
        else:
            kern = g1.rightKerningForLayer_(g2)
        if kern > 10000:
            kern = 0
        # Check sidebearings first (PvB's idea)
        if self.rsb[g1] + self.lsb[g2] + kern > 0:
            return False

        # get the bounds and check them
        bounds1 = g1.bounds
        bounds2 = g2.bounds 

        bounds2 = NSOffsetRect(bounds2, g1.width + kern, 0)
        # check for intersection bounds
        intersectingBounds = NSIntersectsRect(bounds1, bounds2)
        if not intersectingBounds:
            return False

        # create a pen for g1 with a shifted rect, draw the glyph into the pen
        pen1 = self.penCache.get(g1.name, None)
        if not pen1:
            pen1 = SegmentsPen.SegmentsPen(self.font, self._masterID)
            g1.draw(pen1)
            self.penCache[g1.name] = pen1
        
        # create a pen for g2 with a shifted rect and move each found segment with the width and kerning
        
        pen2 = self.penCache.get(g2.name, None)
        if not pen2:
            pen2 = SegmentsPen.SegmentsPen(self.font, self._masterID)
            g2.draw(pen2)
            self.penCache[g2.name] = pen2
        
        offset = g1.width+kern
        
        for segment1 in pen1.segments:
            if not NSIntersectsRect(segment1, bounds2):
                continue
            
            for segment2 in pen2.segments:
                segment2 = [(p[0] + offset, p[1]) for p in segment2]
                if not segmentInBound(segment2, bounds1):
                    continue
                if len(segment1) == 4 and len(segment2) == 4:
                    a1, a2, a3, a4 = segment1
                    b1, b2, b3, b4 = segment2
                    result = GSIntersectBezier3Bezier3(a1, a2, a3, a4, b1, b2, b3, b4)
                elif len(segment1) == 4:
                    p1, p2, p3, p4 = segment1
                    a1, a2 = segment2
                    result = GSIntersectBezier3Line(p1, p2, p3, p4, a1, a2)
                elif len(segment2) == 4:
                    p1, p2, p3, p4 = segment2
                    a1, a2 = segment1
                    result = GSIntersectBezier3Line(p1, p2, p3, p4, a1, a2)
                else:
                    a1, a2 = segment1
                    b1, b2 = segment2
                    result = GSIntersectLineLine(a1, a2, b1, b2)
                    result = result.x < 100000
                if result:
                    return True
        return False

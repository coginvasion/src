# Embedded file name: lib.coginvasion.dna.DNATypesetter
from panda3d.core import *
import math

class DNATypesetter:

    def __init__(self, baseline, dnaStorage):
        self.baseline = baseline
        self.dnaStorage = dnaStorage

    def generate(self, texts):
        root = NodePath('typesetter')
        x = 0.0
        for i, text in enumerate(texts):
            tn = TextNode('text')
            tn.setText(text)
            tn.setTextColor(self.baseline.getColor())
            font = self.dnaStorage.findFont(self.baseline.getCode())
            if font is None:
                font = TextProperties.getDefaultFont()
            tn.setFont(font)
            if i == 0 and 'b' in self.baseline.flags:
                tn.setTextScale(1.5)
            np = root.attachNewNode(tn)
            np.setScale(self.baseline.scale)
            np.setDepthWrite(0)
            if i & 1:
                np.setPos(x + self.baseline.stumble, 0, self.baseline.stomp)
                np.setR(-self.baseline.wiggle)
            else:
                np.setPos(x - self.baseline.stumble, 0, -self.baseline.stomp)
                np.setR(self.baseline.wiggle)
            x += tn.getWidth() * np.getSx() + self.baseline.kern

        for child in root.getChildren():
            child.setX(child.getX() - x / 2)

        if self.baseline.width != 0.0 and self.baseline.height != 0.0:
            ellipse = DNAEllipseFormatter(self.baseline)
            ellipse.process(root)
        for np in root.findAllMatches('**/+TextNode'):
            tn = np.node().generate()
            np2 = np.getParent().attachNewNode(tn)
            np2.setTransform(np.getTransform())
            np.removeNode()

        root.flattenStrong()
        if root.getNumChildren():
            return root.getChild(0)
        else:
            return
            return


class DNAEllipseFormatter:

    def __init__(self, baseline):
        self.baseline = baseline
        self.a = self.baseline.width / 2.0
        self.b = self.baseline.height / 2.0

    def arc(self, x):
        return x / self.b

    def process(self, np):
        for node in np.getChildren():
            theta = self.arc(node.getX())
            deviation = node.getY()
            theta += self.baseline.indent * math.pi / 180
            x, y = math.sin(theta) * self.a, (math.cos(theta) - 1) * self.b
            radius = math.sqrt(x * x + y * y)
            if radius > 0.0:
                x *= (radius + deviation) / radius
                y *= (radius + deviation) / radius
            node.setPos(x, 0, y)
            node.setR(node, theta * 180 / math.pi)
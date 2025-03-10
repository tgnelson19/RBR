import pygame
from math import pi
from random import randint

#Whacko sicko mode hardcode that controls the leveling up schema
class LevelingHandler:    
    def __init__(self, tileSize, frameRate, cardColor, sW, sH):
        self.tileSize = tileSize
        self.frameRate = frameRate
        self.sW = sW
        self.sH = sH
        self.cardColor = cardColor
        self.baseColor = pygame.Color(0,0,0)

        # Scale tileSize dynamically
        self.tileSize = min(self.sW, self.sH) / 20  

        # Scale fonts
        self.titleFont = pygame.font.Font("media/coolveticarg.otf", int(self.tileSize * 1.3))
        self.descFont = pygame.font.Font("media/coolveticarg.otf", int(self.tileSize *.7))

        self.textColor = pygame.Color(0,0,0)

        self.update_layout()

        self.firstClick = True

        

        
        self.upgradeRarityColors = {"Common" : pygame.Color(0,0,0), "Rare" : pygame.Color(0,0,200), "Epic" : pygame.Color(128,0,128), "Legendary" : pygame.Color(255, 215, 0), "Mythical" : pygame.Color(255,255,255)}

        #Chance of rarity being dropped (one in #)
        self.upgradeRarityChancesOneIn = {"Common" : 1, "Rare" : 4, "Epic" : 10, "Legendary" : 25, "Mythical" : 100}
        
        #Rarity multiplier for the upgrade's value
        self.upgradeRarity = {"Common" : 1, "Rare" : 2, "Epic" : 3, "Legendary" : 5, "Mythical" : 10}

        self.upgradeRarityListReversed = ["Mythical", "Legendary", "Epic", "Rare", "Common"]
        self.upgradeBasicsMaths = {"addative" : "Addatively", "multiplicative" : "Multiplicatively"}

        self.upgradeTypesList = ["Defense", "Bullet Pierce", "Bullet Count", "Spread Angle", 
                                  "Attack Speed", "Bullet Speed", "Bullet Range", "Bullet Damage", 
                                  "Bullet Size", "Player Speed", "Crit Chance", "Crit Damage", "Aura Size", "Aura Strength"]
        
        #Base values for upgrades at common

        self.upgradeBasicTypesAdd = {"Defense" : 1, "Bullet Pierce" : 0.25, "Bullet Count" : 0.25, "Spread Angle" : pi/8, 
                                  "Attack Speed" : -1, "Bullet Speed" : 4, "Bullet Range" : 100, "Bullet Damage" : 0.25, 
                                  "Bullet Size" : 5, "Player Speed" : 0.25, "Crit Chance" : 0.1, "Crit Damage" : 0.5, "Aura Size" : 10, "Aura Strength" : 1}
        
        self.upgradeBasicTypesMult = {"Defense" : 0.2, "Bullet Pierce" : 0.2, "Bullet Count" : 0.2, "Spread Angle" : 0.2, 
                                  "Attack Speed" : -0.05, "Bullet Speed" : 0.25, "Bullet Range" : 0.25, "Bullet Damage" : 0.2, 
                                  "Bullet Size" : 0.2, "Player Speed" : 0.2, "Crit Chance" : 0.05, "Crit Damage" : 0.2, "Aura Size" : 0.2, "Aura Strength" : 0.2}
        
        self.upgradeBasicTypesMapper = {"Defense" : "defense", "Bullet Pierce" : "bulletPierce", "Bullet Count" : "projectileCount", "Spread Angle" : "azimuthalProjectileAngle", 
                                  "Attack Speed" : "attackCooldownStat", "Bullet Speed" : "bulletSpeed", "Bullet Range" : "bulletRange", "Bullet Damage" : "damage", 
                                  "Bullet Size" : "bulletSize", "Player Speed" : "playerSpeed", "Crit Chance" : "critChance", "Crit Damage" : "critDamage", "Aura Size" : "aura", "Aura Size" : "auraSpeed"}
        
        self.upgradeUniqueTypes = ["healFull"]

        self.leftCardUpgradeRarity = "Common"
        self.leftCardUpgradeMath = "addative"
        self.leftCardUpgradeType = "Bullet Damage"

        self.midCardUpgradeRarity = "Epic"
        self.midCardUpgradeMath = "addative"
        self.midCardUpgradeType = "Bullet Damage"

        self.rightCardUpgradeRarity = "Mythical"
        self.rightCardUpgradeMath = "addative"
        self.rightCardUpgradeType = "Player Speed"

        self.randomizing = False

        self.rarities = [self.leftCardUpgradeRarity, self.midCardUpgradeRarity, self.rightCardUpgradeRarity]
        self.maths = [self.leftCardUpgradeMath, self.midCardUpgradeMath, self.rightCardUpgradeMath]
        self.types = [self.leftCardUpgradeType, self.midCardUpgradeType, self.rightCardUpgradeType]

    def update_layout(self):
        """Recalculate card positions and sizes dynamically."""
        cardWidth = (self.sW - self.tileSize * 5) / 3
        cardHeight = self.sH * .6  # Cards take up 45% of screen height

        cardY = (self.sH - cardHeight) / 2

        self.leftCard = pygame.Rect(self.tileSize * 2, cardY, cardWidth, cardHeight)
        self.midCard = pygame.Rect(self.tileSize * 3 + cardWidth, cardY, cardWidth, cardHeight)
        self.rightCard = pygame.Rect(self.tileSize * 4 + 2 * cardWidth, cardY, cardWidth, cardHeight)


    def drawCards(self, screen):
        """Draw the three cards, keeping the original structure intact but making it resolution-adaptive."""
        for card, rarity, mathType, upgradeType in zip(
            [self.leftCard, self.midCard, self.rightCard],
            [self.leftCardUpgradeRarity, self.midCardUpgradeRarity, self.rightCardUpgradeRarity],
            [self.leftCardUpgradeMath, self.midCardUpgradeMath, self.rightCardUpgradeMath],
            [self.leftCardUpgradeType, self.midCardUpgradeType, self.rightCardUpgradeType]
        ):
            pygame.draw.rect(screen, self.cardColor, card)

            # Title (Rarity)
            textRender = self.titleFont.render(rarity, True, self.upgradeRarityColors[rarity])
            textRect = textRender.get_rect(center=(card.centerx, card.top + card.height * 0.1))  # 10% from top
            screen.blit(textRender, textRect)

            # Upgrade Type
            textRender = self.titleFont.render(upgradeType, True, self.upgradeRarityColors[rarity])
            textRect = textRender.get_rect(center=(card.centerx, card.top + card.height * 0.25))  # 25% from top
            screen.blit(textRender, textRect)

            # Description (Properly placed near the bottom)
            desc_y_start = card.bottom - card.height * 0.3  # 30% up from the bottom
            textRender = self.descFont.render(self.upgradeBasicsMaths[mathType] + " increases", True, self.baseColor)
            textRect = textRender.get_rect(center=(card.centerx, desc_y_start))
            screen.blit(textRender, textRect)

            textRender = self.descFont.render(upgradeType, True, self.baseColor)
            textRect = textRender.get_rect(center=(card.centerx, desc_y_start + self.tileSize * 0.7))  # Small offset
            screen.blit(textRender, textRect)

            # Render Value
            value_y = card.bottom - card.height * 0.05

            if mathType == "addative":
                textRender = self.descFont.render(f"By {1}", True, self.baseColor)  # Placeholder value
            else:
                textRender = self.descFont.render(f"By {1.2}x", True, self.baseColor)  # Placeholder multiplier

            textRect = textRender.get_rect(center=(card.centerx, value_y))
            screen.blit(textRender, textRect)

    def PlayerClicked(self, mouseDown, mouseX, mouseY):
        if (not mouseDown):
            self.firstClick = False

        if (mouseDown and not self.firstClick):
            if(mouseX < self.leftCard.right and mouseX > self.leftCard.left):
                if(mouseY < self.leftCard.bottom and mouseY > self.leftCard.top):
                    self.firstClick = True
                    return "leftCard"
            if(mouseX < self.midCard.right and mouseX > self.midCard.left):
                if(mouseY < self.midCard.bottom and mouseY > self.midCard.top):
                    self.firstClick = True
                    return "midCard"
            if(mouseX < self.rightCard.right and mouseX > self.rightCard.left):
                if(mouseY < self.rightCard.bottom and mouseY > self.rightCard.top):
                    self.firstClick = True
                    return "rightCard"
        else:
            return "none"
        
    def randomizeLevelUp(self):
        
        rarities = [self.leftCardUpgradeRarity, self.midCardUpgradeRarity, self.rightCardUpgradeRarity]
        maths = [self.leftCardUpgradeMath, self.midCardUpgradeMath, self.rightCardUpgradeMath]
        types = [self.leftCardUpgradeType, self.midCardUpgradeType, self.rightCardUpgradeType]

        for card in maths:
            addOrMult = randint(1,2)
            if(addOrMult == 1):
                new = "addative"
            else:
                new = "multiplicative"
            maths[maths.index(card)] = new

        for i, card in enumerate(rarities):
            for rarity in self.upgradeRarityListReversed:
                if (self.upgradeRarityChancesOneIn[rarity] == 1):
                    new = rarity
                    rarities[i] = new
                    break
                else:
                    rarityClick = randint(1, self.upgradeRarityChancesOneIn[rarity])
                    if(rarityClick == 1):
                        new = rarity
                        rarities[i] = new
                        break
                
        for card in types:
            click = randint(0, len(self.upgradeTypesList) - 1)
            new = self.upgradeTypesList[click]
            types[types.index(card)] = new

        self.leftCardUpgradeRarity = rarities[0]
        self.leftCardUpgradeMath = maths[0]
        self.leftCardUpgradeType = types[0]

        self.midCardUpgradeRarity = rarities[1]
        self.midCardUpgradeMath = maths[1]
        self.midCardUpgradeType = types[1]

        self.rightCardUpgradeRarity = rarities[2]
        self.rightCardUpgradeMath = maths[2]
        self.rightCardUpgradeType = types[2]

        self.randomizing = True




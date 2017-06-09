class SearchZone(Comportement):

    interconnection = IntercoI2C() # Instanciates the interconnection class to write the actions to the Arduino

    def recherche():
        global distance
        global target
        #pattern de recherche
        print distance
        if(target==False):
            if(distance>15):
                interconnection.writeNumber(Actions.FORWARD.value)

            elif(distance<=15):
                interconnection.writeNumber(Actions.LEFT.value)
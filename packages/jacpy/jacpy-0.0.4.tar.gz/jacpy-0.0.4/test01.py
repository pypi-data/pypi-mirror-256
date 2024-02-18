from src.jacpy.io import ioUtils

items = ioUtils.dirItems('C:/Users/alber/Desktop/BACKUP ABRIL 2022', ioUtils.DirItemPolicy.AllAlphabetic, ioUtils.DirItemOutputForm.Name, 0, 2)

print(items)
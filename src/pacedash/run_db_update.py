import shutil
import glob
import distutils.dir_util


def update_db():
    shutil.copy2(
        "V:\\Databases\\PaceDashboard.db",
        "E:\\pace_dash\\src\\pacedash\\data\\PaceDashboard.db",
    )
    shutil.copy2(
        "E:\\pace_dash\\src\\pacedash\\data\\users.db", "V:\\Databases\\users.db"
    )
    shutil.copy2(
        "E:\\pace_dash\\src\\pacedash\\data\\log.txt", "V:\\Databases\\log.txt"
    )
    print("Updated DB")


def update_files():
    filelist = glob.glob("V:\\Dashboard\\pace_dash\\src\\pacedash\\*.py")

    for file in filelist:
        shutil.copy2(file, "E:\\pace_dash\\src\\pacedash")

    for folder in ["assets", "pages"]:
        distutils.dir_util.copy_tree(
            f"V:\\Dashboard\\pace_dash\\src\\pacedash\\{folder}",
            f"E:\\pace_dash\\src\\pacedash\\{folder}",
            update=1,
            verbose=1,
        )
    distutils.dir_util.copy_tree(
        "V:\\Dashboard\\pace_dash\\images", "E:\\pace_dash\\images", update=1, verbose=1
    )
    print("Updated Files")


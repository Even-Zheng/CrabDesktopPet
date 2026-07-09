import sys
import os
import traceback

if getattr(sys, 'frozen', False):
    log_dir = os.path.dirname(sys.executable)
else:
    log_dir = os.path.dirname(os.path.abspath(__file__))

log_path = os.path.join(log_dir, "crab_error.log")

def log(msg):
    try:
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(f"{msg}\n")
    except:
        pass

try:
    log("=" * 50)
    log(f"Starting CrabPet")
    log(f"Frozen: {getattr(sys, 'frozen', False)}")
    log(f"Executable: {sys.executable}")
    log(f"Script dir: {os.path.dirname(os.path.abspath(__file__))}")
    
    log("Importing main...")
    from main import CrabPet
    log("Import successful")
    
    if __name__ == "__main__":
        log("Creating CrabPet...")
        pet = CrabPet()
        log("Running CrabPet...")
        sys.exit(pet.run())
        
except Exception as e:
    log(f"FATAL ERROR: {e}")
    log(traceback.format_exc())
    raise
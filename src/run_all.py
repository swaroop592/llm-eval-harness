import subprocess
import sys

def run(cmd):
    print(f"\n>>> {' '.join(cmd)}")
    subprocess.check_call(cmd)

def main():
    config = "configs/mock.yaml"
    run([sys.executable, "-m", "src.run_eval", "--config", config])
    run([sys.executable, "-m", "src.failure_modes"])
    run([sys.executable, "-m", "src.make_manual_audit"])
    run([sys.executable, "-m", "src.analyze_manual_audit"])
    print("\nAll done. See results/results.csv and reports/.")

if __name__ == "__main__":
    main()

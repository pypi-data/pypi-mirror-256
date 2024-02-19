import argparse
import os
import subprocess
import signal

def usage():
    print("Usage: python script.py [-i image] [-u registry_username] [-p registry_password] [-r registry_url] [-l] [-s]")
    print(" -i      The image to apply a STIG to. This is required")
    print(" -u      The username for an image in a private registry. This is optional.")
    print(" -p      The password for an image in a private registry. This is optional.")
    print(" -r      The URL for a private registry. This is optional.")
    print(" -s      Allow insecure registries or registries with custom certs")
    print(" -l      Detected local image. Running in local mode.")
    print(" -h      Print usage info.")
    exit(1)

def main():
    parser = argparse.ArgumentParser(description="Apply STIG to a Docker image.")
    parser.add_argument("-u", dest="username", help="The username for an image in a private registry.")
    parser.add_argument("-p", dest="password", help="The password for an image in a private registry.")
    parser.add_argument("-r", dest="url", help="The URL for a private registry.")
    parser.add_argument("-i", dest="image", help="The image to apply a STIG to. This is required.", required=True)
    parser.add_argument("-l", dest="local", action="store_true", help="Detected local image. Running in local mode.")
    parser.add_argument("-s", dest="insecure", action="store_true", help="Allow insecure registries or registries with custom certs.")
    args = parser.parse_args()

    if not args.image:
        usage()

    dir_name = args.image.replace("/", "-").replace(":", "-")
    os.makedirs(f"stig-results/{dir_name}", exist_ok=True)

    subprocess.run(["docker", "volume", "create", "stig-runner"])

    def cleanup_volume(signum, frame):
        subprocess.run(["docker", "volume", "rm", "stig-runner"])
        exit(1)

    signal.signal(signal.SIGINT, cleanup_volume)

    if args.local:
        print("Detected local image. Running in local mode.")
        subprocess.run(["docker", "save", args.image, "-o", "./local-image.tar.gz"])
        subprocess.run(["docker", "run", "-t", "--rm", "--privileged",
                        "-e", f"SCAN_IMAGE=localhost/{args.image}",
                        "-e", f"INSECURE_REG={args.insecure}",
                        "--name", "stig-runner",
                        "-v", f"{os.getcwd()}/local-image.tar.gz:/etc/local-image.tar.gz:ro",
                        "-v", f"{os.getcwd()}/stig-results/{dir_name}:/tmp",
                        "anchore/static-stig:0.1.8"])
        os.remove("local-image.tar.gz")
    elif not args.username:
        subprocess.run(["docker", "run", "-t", "--rm", "--privileged",
                        "-e", f"SCAN_IMAGE={args.image}",
                        "-e", f"INSECURE_REG={args.insecure}",
                        "--name", "stig-runner",
                        "-v", f"{os.getcwd()}/stig-results/{dir_name}:/tmp",
                        "anchore/static-stig:0.1.8"])
    else:
        subprocess.run(["docker", "run", "-t", "--rm", "--privileged",
                        "-e", f"SCAN_IMAGE={args.image}",
                        "-e", f"INSECURE_REG={args.insecure}",
                        "-e", f"REGISTRY_USERNAME={args.username}",
                        "-e", f"REGISTRY_PASSWORD={args.password}",
                        "-e", f"REGISTRY_URL={args.url}",
                        "--name", "stig-runner",
                        "-v", f"{os.getcwd()}/stig-results/{dir_name}:/tmp",
                        "anchore/static-stig:0.1.8"])

if __name__ == "__main__":
    main()

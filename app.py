import logging
import platform
import setproctitle
import flaskr
import sys

#Todo. app.py에서는 로깅 시스템과 운영체제 기본적인 설정을 여기서 함

def validate_python() -> None:
    """Validate that the right Python version is running."""
    if sys.version_info[:3] < REQUIRED_PYTHON_VER:
        print(
            "ninewatt Device requires at least Python {}.{}.{}".format(
                *REQUIRED_PYTHON_VER
            )
        )
        sys.exit(1)

def main():
    flask_app = flaskr.create_app()
    flask_app.debug = True
    flask_app.run(host="localhost", port="5000")

if __name__ == "__main__":

    if platform.system() == "Linux":
        setproctitle.setproctitle('ninewatt_app')
    
    sys.exit(main())
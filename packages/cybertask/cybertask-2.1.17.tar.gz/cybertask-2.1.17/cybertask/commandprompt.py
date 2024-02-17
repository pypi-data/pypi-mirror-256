from cybertask import config
from cybertask.health_check import HealthCheck
if not hasattr(config, "exit_entry"):
    HealthCheck.setBasicConfig()
    HealthCheck.saveConfig()
    print("Configurations updated!")
HealthCheck.setPrint()
from cybertask.utils.prompts import Prompts
from cybertask.utils.terminal_system_command_prompt import SystemCommandPrompt
import platform

def setOsOpenCmd():
    thisPlatform = platform.system()
    config.thisPlatform = thisPlatform
    if config.terminalEnableTermuxAPI:
        config.open = "termux-share"
    elif thisPlatform == "Linux":
        config.open = "xdg-open"
    elif thisPlatform == "Darwin":
        config.open = "open"
    elif thisPlatform == "Windows":
        config.open = "start"
    # name macOS
    if config.thisPlatform == "Darwin":
        config.thisPlatform = "macOS"

def main():
    config.systemCommandPromptEntry = ""
    config.print = print
    setOsOpenCmd()
    Prompts()
    SystemCommandPrompt().run(allowPathChanges=True)

if __name__ == '__main__':
    main()
#  __  __ _                            __ _     ____       _         __ _ _
# |  \/  (_)_ __   ___  ___ _ __ __ _ / _| |_  |  _ \ __ _| | _____ / _(_) | ___
# | |\/| | | '_ \ / _ \/ __| '__/ _` | |_| __| | |_) / _` | |/ / _ \ |_| | |/ _ \
# | |  | | | | | |  __/ (__| | | (_| |  _| |_  |  _ < (_| |   <  __/  _| | |  __/
# |_|  |_|_|_| |_|\___|\___|_|  \__,_|_|  \__| |_| \_\__,_|_|\_\___|_| |_|_|\___|
#

  #def config
  #  @config ||= YAML.load_file File.join(Rails.root, 'config.yml')
  #end

# TODO move configuration into YML file
def server_nickname
    'sigma'
end

def backup_file
    "#{backup_directory}#{server_nickname}-#{Time.new.strftime("%Y-%m-%d")}.tar.gz"
end

def backup_directory
    "/data/Games/Minecraft/Server\ Backups/#{server_nickname}/"
end

def minecraft_directory
    "/home/#{server_nickname}/minecraft/"
end

def render_directory
    "/srv/http/#{server_nickname}/"
end

def minecraft_version
    '1.7.2'
end

def temporary_world_location
    #used for renders
    '/home/sigma/minecraft-rakefile/world-temp/'
end

def send_command(keys)
    puts "Sending command: '#{keys}' to #{server_nickname}."
    system "tmux send-keys -t #{server_nickname} '#{keys}' C-m"
end

namespace :server do

    desc "Backup the Minecraft Server"
    task :backup do
        send_command('save-off')
        sleep(1)
        send_command('save-all')
        sleep(5)
        system "mkdir", "-p", backup_directory
        system "rm", "-f", backup_file
        system "tar", "czf", backup_file, minecraft_directory
        send_command('save-on')
        sleep(1)
        send_command('say Backup has been completed.')
        #system "find", backup_directory, "-mtime +7", "-exec rm {} -fv \\;"
    end

    desc "Start the Minecraft Server"
    task :start do
        system "tmux new -s #{server_nickname} -d"
        send_command("cd #{minecraft_directory}; java -Xmx1024M -Xms1024M -jar minecraft_server.jar nogui")
        sleep(5)
    end

    desc "Stop the Minecraft Server"
    task :stop do
        send_command('say The server is being shut down in 10 seconds.')
        sleep(10)
        send_command('stop')
        sleep(5)
        send_command('exit')
    end
end

namespace :render do

    task :setup do
        # If current version doesn't exist
        # and change so it doesn't rm each time (change wget to --output-document)
        system "rm", "-rf", "/home/sigma/.minecraft/"
        system "mkdir", "-p", "/home/sigma/.minecraft/"
        system "wget", "https://s3.amazonaws.com/Minecraft.Download/versions/#{minecraft_version}/#{minecraft_version}.jar", "-P", "/home/sigma/.minecraft/versions/#{minecraft_version}/"
        
        if not File.directory?('/home/sigma/minecraft-rakefile/Minecraft-Overviewer')
            system "git", "clone", "https://github.com/overviewer/Minecraft-Overviewer.git", "/home/sigma/minecraft-rakefile/Minecraft-Overviewer/"
        else
            system "git", "-c", "/home/sigma/minecraft-rakefile/Minecraft-Overviewer", "pull"
        end
        system "python2", "/home/sigma/minecraft-rakefile/Minecraft-Overviewer/setup.py", "build"
    end

    desc "Render the Minecraft Server using Minecraft Overviewer"
    task :update => [:setup] do
        # if no render.lock (use same one for render/poi)
        send_command('save-off')
        sleep(1)
        send_command('save-all')
        sleep(5)
        system "mkdir", "-p", "/home/sigma/minecraft-rakefile/world-temp/"
        system "cp", "-pr", "/home/sigma/minecraft/world/", "/home/sigma/minecraft-rakefile/world-temp/"       
        send_command('save-on')
        sleep(1)
        system "python2", "/home/sigma/minecraft-rakefile/Minecraft-Overviewer/overviewer.py", "--config=/home/sigma/minecraft-rakefile/sigma-mco-config.py" 
        system "rm", "-rf", "/home/sigma/minecraft-rakefile/world-temp/"
        send_command("say The render has been updated.")
        sleep(1)
    end

    desc "Update the Points of Interest using Minecraft Overviewer"
    task :poiupdate => [:setup] do
        send_command('save-off')
        sleep(1)
        send_command('save-all')
        sleep(5)
        system "mkdir", "-p", "/home/sigma/minecraft-rakefile/world-temp/"
        system "cp", "-pr", "/home/sigma/minecraft/world/", "/home/sigma/minecraft-rakefile/world-temp/"       
        send_command('save-on')
        sleep(1)
        system "python2", "/home/sigma/minecraft-rakefile/Minecraft-Overviewer/overviewer.py", "--config=/home/sigma/minecraft-rakefile/sigma-mco-config.py", "--genpoi" 
        system "rm", "-rf", "/home/sigma/minecraft-rakefile/world-temp/"
        # if no render.lock
        # Players / Signs with asterisks
    end

end

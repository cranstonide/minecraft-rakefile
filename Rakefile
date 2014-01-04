#  __  __ _                            __ _     ____       _         __ _ _
# |  \/  (_)_ __   ___  ___ _ __ __ _ / _| |_  |  _ \ __ _| | _____ / _(_) | ___
# | |\/| | | '_ \ / _ \/ __| '__/ _` | |_| __| | |_) / _` | |/ / _ \ |_| | |/ _ \
# | |  | | | | | |  __/ (__| | | (_| |  _| |_  |  _ < (_| |   <  __/  _| | |  __/
# |_|  |_|_|_| |_|\___|\___|_|  \__,_|_|  \__| |_| \_\__,_|_|\_\___|_| |_|_|\___|
#

require 'yaml'

def config
    @config ||= YAML.load_file File.join(rakefile_directory, 'config.yml')
end

def server_nickname
    # This is where I could accept input from the arglist to see which server theyd like to manage (?)
    config.keys.first
end

def backup_file
    filename  = "#{server_nickname}-#{Time.new.strftime("%Y-%m-%d")}.tar.gz"
    directory = config[server_nickname].fetch('backup_directory')
    File.expand_path File.join(directory, filename)
end

def minecraft_directory
    File.expand_path config[server_nickname].fetch('minecraft_server_directory')
end

def rakefile_directory
    File.expand_path File.dirname(__FILE__)
end

def render_directory
    File.expand_path File.join(config[server_nickname].fetch('minecraft_version'), server_nickname)
end

def temporary_render_location
    File.expand_path File.join(rakefile_directory, 'world-temp')
end

def minecraft_version
    config[server_nickname].fetch('minecraft_version')
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
        system "mkdir", "-p", File.dirname(backup_file)
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
        current_game_jar = File.expand_path "~/.minecraft/versions/#{minecraft_version}/#{minecraft_version}.jar"
        system "mkdir", "-p", File.dirname(current_game_jar)

        if not File.exists?(current_game_jar)
            system "wget", "https://s3.amazonaws.com/Minecraft.Download/versions/#{minecraft_version}/#{minecraft_version}.jar", "--output-document=#{current_game_jar}"
        end

        if not File.directory?("#{rakefile_directory}/Minecraft-Overviewer")
            system "git", "clone", "https://github.com/overviewer/Minecraft-Overviewer.git", "#{rakefile_directory}/Minecraft-Overviewer/"
        else
            # Don't use keys?
            system "git", "-c", "#{rakefile_directory}/Minecraft-Overviewer", "pull"
        end

        system "python2", "#{rakefile_directory}/Minecraft-Overviewer/setup.py", "build"
    end

    desc "Render the Minecraft Server using Minecraft Overviewer"
    task :update => [:setup] do
        # if no render.lock (use same one for render/poi)
        send_command('save-off')
        sleep(1)
        send_command('save-all')
        sleep(5)
        system "mkdir", "-p", temporary_render_location
        system "cp", "-pr", minecraft_directory, temporary_render_location
        send_command('save-on')
        sleep(1)
        system "python2", "#{rakefile_directory}/Minecraft-Overviewer/overviewer.py", "--config=#{rakefile_directory}/sigma-mco-config.py"
        system "rm", "-rf", temporary_render_location
        send_command("say The render has been updated.")
        sleep(1)
    end

    desc "Update the Points of Interest using Minecraft Overviewer"
    task :poiupdate => [:setup] do
        send_command('save-off')
        sleep(1)
        send_command('save-all')
        sleep(5)
        system "mkdir", "-p", temporary_render_location
        system "cp", "-pr", minecraft_directory, temporary_render_location
        send_command('save-on')
        sleep(1)
        system "python2", "#{rakefile_directory}Minecraft-Overviewer/overviewer.py", "--config=#{rakefile_directory}/sigma-mco-config.py", "--genpoi"
        system "rm", "-rf", temporary_render_location
        # if no render.lock
        # Players / Signs with asterisks
    end

end

#desc "print config"
#task :debug do
#    puts File.split backup_file
#end

#desc "Check 'config.yml' File"
#task :chkcfg do
#    puts "okay"
#end


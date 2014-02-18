Minecraft Rakefile
==================

Setup
-----

Make sure you have *java*, *git*, *ruby*, and *tmux* installed. You should be able to install those through your package manager.

For Minecraft Overviewer you will need *numpy* and *pillow* (provides Imaging.h) for Python.

Clone this repository. Since I have a special `minecraft` user I'll use the home directory, but you can chose whichever directory you'd like.

    $ cd ~
    $ git clone https://github.com/cranstonide/minecraft-rakefile.git

Copy config.yml.example to config.yml and then edit the configuration portion of the `config.yml` to meet your specific needs. Replace "sigma" with your server nickname.

    $ cp config.yml.example config.yml
    $ vim config.yml

Copy myworld-mco-config.py.example to world-mco-config.py ('world' should match your server_nickname) and then edit the directory paths to meet your specific needs.

    $ cp myworld-mco-config.py.example myworld-mco-config.py
    $ vim myworld-mco-config.py

Add cron entries to automate tasks. You can edit your crontab by running `crontab -e`; for more information on cron, check out the [Wikipedia article on cron](http://en.wikipedia.org/wiki/Cron).

    0    0    *     *    *    rake -f ~/minecraft-rakefile/Rakefile server:backup
    0    */6  *     *    *    rake -f ~/minecraft-rakefile/Rakefile render:update
    */10 *    *     *    *    rake -f ~/minecraft-rakefile/Rakefile render:poiupdate

Manually Running Tasks
----------------------

If you wish to manually run tasks, you can see your options by running:

    $ rake -f ~/minecraft-rakefile/Rakefile -T

And then pick your option:

    $ rake -f ~/minecraft-rakefile/Rakefile server:stop

If you don't want to type `-f ~/minecraft-rakefile/Rakefile`, you can `cd ~/minecraft-rakefile/` and run `rake server:stop`. For more information on Rakefiles, view [the documentation](http://rake.rubyforge.org/).

Under The Hood
--------------
The following applications are used:

* [Minecraft](https://minecraft.net/)
* [Minecraft-Overviewer](http://overviewer.org/)
* [Rake (Ruby)](http://rake.rubyforge.org/)
* [Tmux](http://tmux.sourceforge.net/)


To Do:
------

* Spend more time documenting instructions
* move configuration into yml file

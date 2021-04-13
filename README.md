# cmus-rpcd
cmus-rpcd is a small daemon that allows you to display the song you are currently listening to, as well as other information, through Discord's Rich Presence. It automatically refreshes settings, so you do not need to restart the daemon to get changes to your presence. It also comes with lots of customization options for your presence.

![GIF Demonstration](./images/demonstration_gif.gif)

## How to use
cmus-rpcd is quite simple to setup. cmus-rpcd currently does not launch itself as a service for Systemd, however this is a planned feature for the future. Currently, you must launch the script manually, or find a way to do this on startup. Usually, this is achieved through your window manager, or through some other way if you are using a desktop environment.

However, there is some installation needed on your end. All you must do is install a few packages. The packages are:
* setproctitle
* pypresence
* psutil
</br>
And that is it! You can then launch the program, and it will be displayed on your profile. 

## Configuration
cmus-rpcd can be easily customized. It comes with many options to customize the look of your presence. Your settings file is generated automatically by the daemon in the folder you installed it in. The settings separated by a new line should not be modified, but can be if you know what you are doing.

| Setting          | Functionality 				          |  Type   |
|------------------|------------------------------------------------------|---------|
| change_increment | Time interval between status updates.                | Integer |
| state_format     | The string used to format state information.         | String  |
| details_format   | The string used to format details information.	      | String  |
| progress_format  | The string used to format the song progress.         | String  |
| duration_format  | The string used to format the song duration.         | String  |

## Format Specifiers
cmus-rpcd also has format specifiers that can be applied to the state, and the details. They are:
| Specifier     | Meaning                                                 |
|---------------|------------------------------------------------------   |
| {artist}      | The artist of the song.                                 |
| {album}       | The album of the song.                                  |
| {title}       | The title of the song.                                  |
| {status}      | The title of the song.                                  |
| {tracknum}    | The track number of the song.                           |
| {shuffle}     | Whether or not shuffle is on.                           |
| {repeat}      | Whether or not a repeating is enabled.                  |
| {current}     | Whether or not the current song is repeating.           |
| {playlibrary} | Whether or not the song is playing from the library.    |
| {playsorted}  | Whether or not the playing mode is sorted.              |
| {progress}    | Time left in the song. Formatted by progress_format.    |
| {duration}    | Total time of the song. Formatted by duration_format.   |
| {progpercent} | Time left in the song on a percent scale.               |
| {{}           | An escaped opening curly brace.                         |
| {}}           | An escaped closing curly brace.                         |

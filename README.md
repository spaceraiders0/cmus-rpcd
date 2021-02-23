# cmus-rpcd
cmus-rpcd is a small daemon that allows you to display the song you are currently listening to, as well as other information, through Discord's Rich Presence. It automatically refreshes settings, so you do not need to restart the daemon to get changes to your presence. It also comes with lots of customization options for your presence.

## How to use
cmus-rpcd is quite simple to setup. cmus-rpcd currently does not launch itself as a service for Systemd, however this is a planned feature for the future. Currently, you must launch the script manually, or find a way to do this on startup. Usually, this is achieved through your window manager, or through some other way if you are using a desktop environment.

However, there is some installation needed on your end. All you must do is install a few packages. The packages are:
* setproctitle
* pypresence
* psutil
And that is it! You can then launch the program, and it will be displayed on your profile. 

## Configuration
cmus-rpcd can be easily customized. It comes with many options to customize the look of your presence. Your settings file is generated automatically by the daemon in the folder you installed it in. The settings separated by a new line should not be modified, but can be if you know what you are doing.

| Setting          | Functionality 				          |  Type   |
|------------------|------------------------------------------------------|---------|
| UPDATE_TIME      | Time interval between status updates.                | Integer |
| STATE_FORMAT     | The string used to format state information.         | String  |
| DETAILS_FORMAT   | The string used to format details information.	  | String  |
| PROGRESS_FORMAT  | The string used to format the song progress.         | String  |
| DURATION_FORMAT  | The string used to format the song duration.         | String  |
| INCLUDE_STATUS   | Whether or not to show the status. 		  | Boolean |
| INCLUDE_DETAILS  | Whether or not to show the details.	          | Boolean |

## Format Specifiers
cmus-rpcd also has format specifiers that can be applied to the state, and the details. They are:
| Specifier     | Meaning                                     |
|---------------|---------------------------------------------|
| {name}        | The name of the current song.               |
| {status}      | The playing state of the song.              |
| {repeat}      | Whether or not the song is repeating.       |
| {artist}      | The name of the artist of the current song. |
| {album}       | The name of the album the song is in.       |
| {title}       | The title of the song playing.              |
| {tracknumber} | The track number of the playing song.       |
| {progress}    | The formatted progress through the song.    |
| {duration}    | The formatted duration of the song.         |

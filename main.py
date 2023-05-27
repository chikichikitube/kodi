# Author: Abed_Sako
# Created on: 27.05.2023

import sys
from urllib.parse import urlencode, parse_qsl
import xbmcgui
import xbmcplugin
import requests

# Get the plugin url in plugin:// notation.
_URL = sys.argv[0]
# Get the plugin handle as an integer number.
_HANDLE = int(sys.argv[1])

BASEURL='https://vtr.chikichiki.tube/'

CATEGORIES = ['Channels','Most viewed','Recent','Search']

PAGINGSCREEN = ['ChannelVideos','playlists','playlistVideos']



def get_url(**kwargs):
    return '{}?{}'.format(_URL, urlencode(kwargs))


def get_categories():
    return CATEGORIES

def get_channels():

    req = requests.get(BASEURL+'api/v1/video-channels')
    channels = [[],[],[]]
    
    for indx,item in enumerate(req.json()["data"]):
        if req.json()["data"][indx]["displayName"] == "wa" or req.json()["data"][indx]["displayName"] == "Main root channel":
            continue
    
    
    
        #Channel name
        channels[0].append(req.json()["data"][indx]["displayName"])
        
        #Channel banner
        channels[1].append(BASEURL + req.json()["data"][indx]["banner"]["path"])
        
        #channel handle
        channels[2].append(req.json()["data"][indx]["name"])

   
    return channels
    
def get_channel_playlists(channelHandle,start):
    req = requests.get(BASEURL+'api/v1/video-channels/'+channelHandle+'/video-playlists?count=25&start='+str(start))
    playlists = [[],[],[]]

    for indx,item in enumerate(req.json()["data"]):

        #playlist uuid
        playlists[0].append(req.json()["data"][indx]["uuid"])
        
        #playlist name
        playlists[1].append(req.json()["data"][indx]["displayName"])
        
        #playlist thumbnail
        playlists[2].append(BASEURL + req.json()["data"][indx]["thumbnailPath"])
        
    return playlists

def get_channel_videos(channelHandle,start):
    req = requests.get(BASEURL+'api/v1/video-channels/'+channelHandle+'/videos?start='+str(start)+'&count=25')
    channelVideos = [[],[],[]]
    
    
    for indx,item in enumerate(req.json()["data"]):

        #Video UUID
        channelVideos[0].append(req.json()["data"][indx]["uuid"])
        
        #video name
        channelVideos[1].append(req.json()["data"][indx]["name"])

        #Video Thumbnail path
        channelVideos[2].append(BASEURL + req.json()["data"][indx]["thumbnailPath"])
     

    return channelVideos
    
def get_playlist_videos(playlistID,start):

    req = requests.get(BASEURL+'api/v1/video-playlists/'+playlistID+'/videos?count=25&start='+str(start))
    playlistVideos = [[],[],[]]
    
    
    for indx,item in enumerate(req.json()["data"]):

        #Video UUID
        playlistVideos[0].append(req.json()["data"][indx]["video"]["uuid"])
     
        #Video name
        playlistVideos[1].append(req.json()["data"][indx]["video"]["name"])
        
        #video thumbnail
        playlistVideos[2].append(BASEURL + req.json()["data"][indx]["video"]["thumbnailPath"])

    return playlistVideos
    
    
def get_videos(sort):
    req = requests.get(BASEURL+'api/v1/videos?sort='+sort+'&count=15')
    videos = [[],[],[]]
    
    
    for indx,item in enumerate(req.json()["data"]):

        #Video UUID
        videos[0].append(req.json()["data"][indx]["uuid"])
     
        #Video name
        videos[1].append(req.json()["data"][indx]["name"])
        
        #video thumbnail
        videos[2].append(BASEURL + req.json()["data"][indx]["thumbnailPath"])

    return videos

def search_videos(searchString):
    req = requests.get(BASEURL+'api/v1/search/videos?search='+searchString+'&count=30')
    
    videos = [[],[],[]]
    
    
    for indx,item in enumerate(req.json()["data"]):

        #Video UUID
        videos[0].append(req.json()["data"][indx]["uuid"])
     
        #Video name
        videos[1].append(req.json()["data"][indx]["name"])
        
        #video thumbnail
        videos[2].append(BASEURL + req.json()["data"][indx]["thumbnailPath"])

    return videos
    
def get_video_path(uuid):
    
    req = requests.get(BASEURL+'api/v1/videos/'+uuid)
    videoPath = req.json()["streamingPlaylists"][0]["playlistUrl"]

    return videoPath

def list_categories():
    # Set plugin category. It is displayed in some skins as the name
    # of the current section.
    xbmcplugin.setPluginCategory(_HANDLE, 'Home')
    # Set plugin content. It allows Kodi to select appropriate views
    # for this type of content.
    xbmcplugin.setContent(_HANDLE, 'videos')
    # Get video categories
    categories = get_categories()
    # Iterate through categories
    for category in categories:
        # Create a list item with a text label and a thumbnail image.
        list_item = xbmcgui.ListItem(label=category)

        
        # Set additional info for the list item.
        # Here we use a category name for both properties for for simplicity's sake.
        # setInfo allows to set various information for an item.
        # For available properties see the following link:
        # https://codedocs.xyz/xbmc/xbmc/group__python__xbmcgui__listitem.html#ga0b71166869bda87ad744942888fb5f14
        # 'mediatype' is needed for a skin to display info for this ListItem correctly.
        list_item.setInfo('video', {'title': category,
                                    'genre': category,
                                    'mediatype': 'video'})
        # Create a URL for a plugin recursive call.
        # Example: plugin://plugin.video.example/?action=listing&category=Animals
        url = get_url(action='listing', category=category)
        # is_folder = True means that this item opens a sub-list of lower level items.
        is_folder = True
        # Add our item to the Kodi virtual folder listing.
        xbmcplugin.addDirectoryItem(_HANDLE, url, list_item, is_folder)
        
    # Add a sort method for the virtual folder items (alphabetically, ignore articles)
    xbmcplugin.addSortMethod(_HANDLE, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
    # Finish creating a virtual folder.
    xbmcplugin.endOfDirectory(_HANDLE)

def list_channels():
    # Set plugin category. It is displayed in some skins as the name
    # of the current section.
    xbmcplugin.setPluginCategory(_HANDLE, 'Channels')
    # Set plugin content. It allows Kodi to select appropriate views
    # for this type of content.
    xbmcplugin.setContent(_HANDLE, 'videos')
    # Get video channels
    channels = get_channels()
    # Iterate through channels
    for indx,channelName in enumerate(channels[0]):
        # Create a list item with a text label and a thumbnail image.
        list_item = xbmcgui.ListItem(label=channelName)

        
      
        list_item.setArt({'thumb': channels[1][indx], 'icon': channels[1][indx], 'fanart': channels[1][indx]})

        # Set additional info for the list item.
        # Here we use a category name for both properties for for simplicity's sake.
        # setInfo allows to set various information for an item.
        # For available properties see the following link:
        # https://codedocs.xyz/xbmc/xbmc/group__python__xbmcgui__listitem.html#ga0b71166869bda87ad744942888fb5f14
        # 'mediatype' is needed for a skin to display info for this ListItem correctly.
        list_item.setInfo('video', {'title': channelName,
                                    'genre': channelName,
                                    'mediatype': 'video'})
        # Create a URL for a plugin recursive call.
        # Example: plugin://plugin.video.example/?action=listing&category=Animals
        url = get_url(action='listing', channel=channels[2][indx])
        # is_folder = True means that this item opens a sub-list of lower level items.
        is_folder = True
        # Add our item to the Kodi virtual folder listing.
        xbmcplugin.addDirectoryItem(_HANDLE, url, list_item, is_folder)
        
    # Add a sort method for the virtual folder items (alphabetically, ignore articles)
    xbmcplugin.addSortMethod(_HANDLE, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
    # Finish creating a virtual folder.
    xbmcplugin.endOfDirectory(_HANDLE)
    
    
def list_channel_choice(channel):
    """
    Create the list of channel choice in the Kodi interface.
    """
    # Set plugin category. It is displayed in some skins as the name
    # of the current section.
    xbmcplugin.setPluginCategory(_HANDLE, 'ChannelsChoice')
    # Set plugin content. It allows Kodi to select appropriate views
    # for this type of content.
    xbmcplugin.setContent(_HANDLE, 'videos')
    # Get channel choices
    choices = ['Videos','Playlists']
    # Iterate through channel choices
    for indx,choice in enumerate(choices):
        # Create a list item with a text label and a thumbnail image.
        list_item = xbmcgui.ListItem(label=choice)

           
        # Set additional info for the list item.
            # Here we use a category name for both properties for for simplicity's sake.
            # setInfo allows to set various information for an item.
            # For available properties see the following link:
            # https://codedocs.xyz/xbmc/xbmc/group__python__xbmcgui__listitem.html#ga0b71166869bda87ad744942888fb5f14
            # 'mediatype' is needed for a skin to display info for this ListItem correctly.
        list_item.setInfo('video', {'title': choice,
                                    'genre': choice,
                                    'mediatype': 'video'})
            # Create a URL for a plugin recursive call.
            # Example: plugin://plugin.video.example/?action=listing&category=Animals
        url = get_url(action='listing', choice=choice , channelHandle = channel)
            # is_folder = True means that this item opens a sub-list of lower level items.
        is_folder = True
            # Add our item to the Kodi virtual folder listing.
        xbmcplugin.addDirectoryItem(_HANDLE, url, list_item, is_folder)
            
        # Add a sort method for the virtual folder items (alphabetically, ignore articles)
    xbmcplugin.addSortMethod(_HANDLE, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
        # Finish creating a virtual folder.
    xbmcplugin.endOfDirectory(_HANDLE)


def list_channel_playlists(channelHandle,start):
    """
    Create the list of channel playlists in the Kodi interface.
    """
    # Set plugin category. It is displayed in some skins as the name
    # of the current section.
    xbmcplugin.setPluginCategory(_HANDLE, 'ChannelPlaylists')
    # Set plugin content. It allows Kodi to select appropriate views
    # for this type of content.
    xbmcplugin.setContent(_HANDLE, 'videos')
    # Get channel playlists
    playlists = get_channel_playlists(channelHandle,start)
    # Iterate through channel playlists
    
    #add next page item
    playlists[0].append(-1)
    playlists[1].append('‎ Next Page‎ ')
    playlists[2].append('')
    
    for indx,playlist in enumerate(playlists[0]):
        # Create a list item with a text label and a thumbnail image.
        list_item = xbmcgui.ListItem(label=playlists[1][indx])

        list_item.setArt({'thumb': playlists[2][indx], 'icon': playlists[2][indx], 'fanart': playlists[2][indx]})
        # Set additional info for the list item.
            # Here we use a category name for both properties for for simplicity's sake.
            # setInfo allows to set various information for an item.
            # For available properties see the following link:
            # https://codedocs.xyz/xbmc/xbmc/group__python__xbmcgui__listitem.html#ga0b71166869bda87ad744942888fb5f14
            # 'mediatype' is needed for a skin to display info for this ListItem correctly.
        list_item.setInfo('video', {'title': playlists[1][indx],
                                    'mediatype': 'video'})
            # Create a URL for a plugin recursive call.
            # Example: plugin://plugin.video.example/?action=listing&category=Animals
        url = get_url(action='listing', playlist=playlists[0][indx])
            # is_folder = True means that this item opens a sub-list of lower level items.
        is_folder = True
        
        if playlist == -1:
            url = get_url(action='nextPage',channelHandle = channelHandle, screen=PAGINGSCREEN[1],startNumber = int(start)+25)
            is_folder = True
        
            # Add our item to the Kodi virtual folder listing.
        xbmcplugin.addDirectoryItem(_HANDLE, url, list_item, is_folder)
            
        # Add a sort method for the virtual folder items (alphabetically, ignore articles)
        #xbmcplugin.addSortMethod(_HANDLE, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
        # Finish creating a virtual folder.
    xbmcplugin.endOfDirectory(_HANDLE)
    


def list_playlist_videos(playlistID,start):
    """
    Create the list of playable videos in the Kodi interface.

    :param category: Category name
    :type category: str
    """
    # Set plugin category. It is displayed in some skins as the name
    # of the current section.
    xbmcplugin.setPluginCategory(_HANDLE, "Videos")
    # Set plugin content. It allows Kodi to select appropriate views
    # for this type of content.
    xbmcplugin.setContent(_HANDLE, 'videos')
    # Get the list of videos in the category.
    videos = get_playlist_videos(playlistID,start)

    #add next page item
    videos[0].append(-1)
    videos[1].append('‎ Next Page‎ ')
    videos[2].append('')

    # Iterate through videos.
    for indx,video in enumerate(videos[0]):
        
    
        # Create a list item with a text label and a thumbnail image.
        list_item = xbmcgui.ListItem(label=videos[1][indx])
        # Set additional info for the list item.
        # 'mediatype' is needed for skin to display info for this ListItem correctly.
        list_item.setInfo('video', {'title': videos[1][indx],
                                    'mediatype': 'video'})
        # Set graphics (thumbnail, fanart, banner, poster, landscape etc.) for the list item.
        # Here we use the same image for all items for simplicity's sake.
        # In a real-life plugin you need to set each image accordingly.
        list_item.setArt({'thumb': videos[2][indx], 'icon': videos[2][indx], 'fanart': videos[2][indx]})
        # Set 'IsPlayable' property to 'true'.
        # This is mandatory for playable items!
        list_item.setProperty('IsPlayable', 'true')
        # Create a URL for a plugin recursive call.
        # Example: plugin://plugin.video.example/?action=play&video=http://www.vidsplay.com/wp-content/uploads/2017/04/crab.mp4
        url = get_url(action='play', video=videos[0][indx])
        # Add the list item to a virtual Kodi folder.
        # is_folder = False means that this item won't open any sub-list.
        is_folder = False
        
        if video == -1:
            url = get_url(action='nextPage',playlistID = playlistID, screen=PAGINGSCREEN[2],startNumber = int(start)+25)
            is_folder = True
        
        # Add our item to the Kodi virtual folder listing.
        xbmcplugin.addDirectoryItem(_HANDLE, url, list_item, is_folder)
    # Add a sort method for the virtual folder items (alphabetically, ignore articles)
    #xbmcplugin.addSortMethod(_HANDLE, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
    # Finish creating a virtual folder.
    xbmcplugin.endOfDirectory(_HANDLE)
    

def list_channel_videos(channelHandle,start):
    """
    Create the list of playable videos in the Kodi interface.

    :param category: Category name
    :type category: str
    """
    # Set plugin category. It is displayed in some skins as the name
    # of the current section.
    xbmcplugin.setPluginCategory(_HANDLE, "Videos")
    # Set plugin content. It allows Kodi to select appropriate views
    # for this type of content.
    xbmcplugin.setContent(_HANDLE, 'videos')
    # Get the list of videos in the category.
    videos = get_channel_videos(channelHandle,start)


    #add next page item
    videos[0].append(-1)
    videos[1].append('‎ Next Page‎ ')
    videos[2].append('')

    # Iterate through videos.
    for indx,video in enumerate(videos[0]):
        
    
        # Create a list item with a text label and a thumbnail image.
        list_item = xbmcgui.ListItem(label=videos[1][indx])
        # Set additional info for the list item.
        # 'mediatype' is needed for skin to display info for this ListItem correctly.
        list_item.setInfo('video', {'title': videos[1][indx],
                                    'mediatype': 'video'})
        # Set graphics (thumbnail, fanart, banner, poster, landscape etc.) for the list item.
        # Here we use the same image for all items for simplicity's sake.
        # In a real-life plugin you need to set each image accordingly.
        list_item.setArt({'thumb': videos[2][indx], 'icon': videos[2][indx], 'fanart': videos[2][indx]})
        # Set 'IsPlayable' property to 'true'.
        # This is mandatory for playable items!
        list_item.setProperty('IsPlayable', 'true')
        # Create a URL for a plugin recursive call.
        # Example: plugin://plugin.video.example/?action=play&video=http://www.vidsplay.com/wp-content/uploads/2017/04/crab.mp4
        url = get_url(action='play', video=videos[0][indx])
        
        
        # Add the list item to a virtual Kodi folder.
        # is_folder = False means that this item won't open any sub-list.
        is_folder = False
        
        if video == -1:
            url = get_url(action='nextPage',channelHandle = channelHandle, screen=PAGINGSCREEN[0],startNumber = int(start)+25)
            is_folder = True
        
        # Add our item to the Kodi virtual folder listing.
        xbmcplugin.addDirectoryItem(_HANDLE, url, list_item, is_folder)
    # Add a sort method for the virtual folder items (alphabetically, ignore articles)
    #xbmcplugin.addSortMethod(_HANDLE, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
    # Finish creating a virtual folder.
    xbmcplugin.endOfDirectory(_HANDLE)
    
    

def list_popular_videos():


    """
    Create the list of playable videos in the Kodi interface.

    :param category: Category name
    :type category: str
    """
    # Set plugin category. It is displayed in some skins as the name
    # of the current section.
    xbmcplugin.setPluginCategory(_HANDLE, "Videos")
    # Set plugin content. It allows Kodi to select appropriate views
    # for this type of content.
    xbmcplugin.setContent(_HANDLE, 'videos')
    # Get the list of videos in the category.
    videos = get_videos('-views')

    # Iterate through videos.
    for indx,video in enumerate(videos[0]):
        
    
        # Create a list item with a text label and a thumbnail image.
        list_item = xbmcgui.ListItem(label=videos[1][indx])
        # Set additional info for the list item.
        # 'mediatype' is needed for skin to display info for this ListItem correctly.
        list_item.setInfo('video', {'title': videos[1][indx],
                                    'mediatype': 'video'})
        # Set graphics (thumbnail, fanart, banner, poster, landscape etc.) for the list item.
        # Here we use the same image for all items for simplicity's sake.
        # In a real-life plugin you need to set each image accordingly.
        list_item.setArt({'thumb': videos[2][indx], 'icon': videos[2][indx], 'fanart': videos[2][indx]})
        # Set 'IsPlayable' property to 'true'.
        # This is mandatory for playable items!
        list_item.setProperty('IsPlayable', 'true')
        # Create a URL for a plugin recursive call.
        # Example: plugin://plugin.video.example/?action=play&video=http://www.vidsplay.com/wp-content/uploads/2017/04/crab.mp4
        url = get_url(action='play', video=videos[0][indx])
        # Add the list item to a virtual Kodi folder.
        # is_folder = False means that this item won't open any sub-list.
        is_folder = False
        # Add our item to the Kodi virtual folder listing.
        xbmcplugin.addDirectoryItem(_HANDLE, url, list_item, is_folder)
    # Add a sort method for the virtual folder items (alphabetically, ignore articles)
    #xbmcplugin.addSortMethod(_HANDLE, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
    # Finish creating a virtual folder.
    xbmcplugin.endOfDirectory(_HANDLE)

def list_recent_videos():
    """
    Create the list of playable videos in the Kodi interface.

    :param category: Category name
    :type category: str
    """
    # Set plugin category. It is displayed in some skins as the name
    # of the current section.
    xbmcplugin.setPluginCategory(_HANDLE, "Videos")
    # Set plugin content. It allows Kodi to select appropriate views
    # for this type of content.
    xbmcplugin.setContent(_HANDLE, 'videos')
    # Get the list of videos in the category.
    videos = get_videos('-publishedAt')
    

    # Iterate through videos.
    for indx,video in enumerate(videos[0]):
        
    
        # Create a list item with a text label and a thumbnail image.
        list_item = xbmcgui.ListItem(label=videos[1][indx])
        # Set additional info for the list item.
        # 'mediatype' is needed for skin to display info for this ListItem correctly.
        list_item.setInfo('video', {'title': videos[1][indx],
                                    'mediatype': 'video'})
        # Set graphics (thumbnail, fanart, banner, poster, landscape etc.) for the list item.
        # Here we use the same image for all items for simplicity's sake.
        # In a real-life plugin you need to set each image accordingly.
        list_item.setArt({'thumb': videos[2][indx], 'icon': videos[2][indx], 'fanart': videos[2][indx]})
        # Set 'IsPlayable' property to 'true'.
        # This is mandatory for playable items!
        list_item.setProperty('IsPlayable', 'true')
        # Create a URL for a plugin recursive call.
        # Example: plugin://plugin.video.example/?action=play&video=http://www.vidsplay.com/wp-content/uploads/2017/04/crab.mp4
        url = get_url(action='play', video=videos[0][indx])
        
        
        # Add the list item to a virtual Kodi folder.
        # is_folder = False means that this item won't open any sub-list.
        is_folder = False
        # Add our item to the Kodi virtual folder listing.
        xbmcplugin.addDirectoryItem(_HANDLE, url, list_item, is_folder)
    # Add a sort method for the virtual folder items (alphabetically, ignore articles)
    #xbmcplugin.addSortMethod(_HANDLE, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
    # Finish creating a virtual folder.
    xbmcplugin.endOfDirectory(_HANDLE)
   
    
def list_search_videos(searchString):
    """
    Create the list of playable videos in the Kodi interface.

    :param category: Category name
    :type category: str
    """
    # Set plugin category. It is displayed in some skins as the name
    # of the current section.
    xbmcplugin.setPluginCategory(_HANDLE, "Videos")
    # Set plugin content. It allows Kodi to select appropriate views
    # for this type of content.
    xbmcplugin.setContent(_HANDLE, 'videos')
    # Get the list of videos in the category.
    videos = search_videos(searchString)

    # Iterate through videos.
    for indx,video in enumerate(videos[0]):
        
    
        # Create a list item with a text label and a thumbnail image.
        list_item = xbmcgui.ListItem(label=videos[1][indx])
        # Set additional info for the list item.
        # 'mediatype' is needed for skin to display info for this ListItem correctly.
        list_item.setInfo('video', {'title': videos[1][indx],
                                    'mediatype': 'video'})
        # Set graphics (thumbnail, fanart, banner, poster, landscape etc.) for the list item.
        # Here we use the same image for all items for simplicity's sake.
        # In a real-life plugin you need to set each image accordingly.
        list_item.setArt({'thumb': videos[2][indx], 'icon': videos[2][indx], 'fanart': videos[2][indx]})
        # Set 'IsPlayable' property to 'true'.
        # This is mandatory for playable items!
        list_item.setProperty('IsPlayable', 'true')
        # Create a URL for a plugin recursive call.
        # Example: plugin://plugin.video.example/?action=play&video=http://www.vidsplay.com/wp-content/uploads/2017/04/crab.mp4
        url = get_url(action='play', video=videos[0][indx])
        # Add the list item to a virtual Kodi folder.
        # is_folder = False means that this item won't open any sub-list.
        is_folder = False
        # Add our item to the Kodi virtual folder listing.
        xbmcplugin.addDirectoryItem(_HANDLE, url, list_item, is_folder)
    # Add a sort method for the virtual folder items (alphabetically, ignore articles)
    #xbmcplugin.addSortMethod(_HANDLE, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
    # Finish creating a virtual folder.
    xbmcplugin.endOfDirectory(_HANDLE)

def search():
    keyboard = xbmc.Keyboard("","Search",False)
    keyboard.doModal()
    if keyboard.isConfirmed():
        list_search_videos(keyboard.getText())
    return None

def play_video(uuid):
    """
    Play a video by the provided path.

    :param path: Fully-qualified video URL
    :type path: str
    """
    # Create a playable item with a path to play.
    play_item = xbmcgui.ListItem(path=get_video_path(uuid))
    # Pass the item to the Kodi player.
    xbmcplugin.setResolvedUrl(_HANDLE, True, listitem=play_item)


def router(paramstring):
    """
    Router function that calls other functions
    depending on the provided paramstring

    :param paramstring: URL encoded plugin paramstring
    :type paramstring: str
    """
    # Parse a URL-encoded paramstring to the dictionary of
    # {<parameter>: <value>} elements
    params = dict(parse_qsl(paramstring))
    # Check the parameters passed to the plugin
    if params:
        if params['action'] == 'listing':
            

            

            #CATEGORY
            if params.get('category') == CATEGORIES[0]:
                list_channels()
            elif params.get('category') == CATEGORIES[1]:
                list_popular_videos()
            elif params.get('category') == CATEGORIES[2]:
                list_recent_videos()
            elif params.get('category') == CATEGORIES[3]:
                search()


            #CHANNEL
            if params.get('channel'):
                list_channel_choice(params.get('channel'))
                
            
            #Channel Choice
            if params.get('choice') == 'Videos':
                list_channel_videos(params.get('channelHandle'),0)
                    
            elif params.get('choice') == 'Playlists':
                list_channel_playlists(params.get('channelHandle'),0)
            
            
            #Playlist
            if params.get('playlist'):
                list_playlist_videos(params.get('playlist'),0)
            
            
            
            
            # Display the list of videos in a provided category.
            #list_videos(params['category'])
        elif params['action'] == 'play':
            # Play a video from a provided URL.
            play_video(params['video'])
            
        elif params['action'] == 'nextPage':
            if params['screen'] == PAGINGSCREEN[0]:
                list_channel_videos(params.get('channelHandle'),params.get('startNumber'))
            elif params['screen'] == PAGINGSCREEN[1]:
                list_channel_playlists(params.get('channelHandle'),params.get('startNumber'))
            elif params['screen'] == PAGINGSCREEN[2]:
                list_playlist_videos(params.get('playlistID'),params.get('startNumber'))
            
            
            
        else:
            # If the provided paramstring does not contain a supported action
            # we raise an exception. This helps to catch coding errors,
            # e.g. typos in action names.
            raise ValueError('Invalid paramstring: {}!'.format(paramstring))
    else:
        # If the plugin is called from Kodi UI without any parameters,
        # display the list of video categories
        list_categories()


if __name__ == '__main__':
    # Call the router function and pass the plugin call parameters to it.
    # We use string slicing to trim the leading '?' from the plugin call paramstring
    router(sys.argv[2][1:])
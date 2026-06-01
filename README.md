## Background

I'd like to listen to more albums but I'm not great at choosing which albums I should give a try. I'd like to a playlist that shuffles itself every day while keeping albums intact within the playlist. That way, I can listen to whatever is at the top and limit the number of choices I have to make.

I would also like to reorder playlists based on things like a hash of the song's ID. That way, the playlist will likely appear more random and thus be more aesthetically pleasing to scroll through.

## Spotify API

To reorder playlist items on Spotify, you have to make a call to the 'Update Playlist Items' endpoint for that particular playlist. The body accepts three parameters of interest:

 * `range_start` - The position of the first item in the sequence you'd like to move
 * `range_length` - The number of items in the sequence you'd like to move (max of 100)
 * `insert_before` - The current position you would like to move the sequence to

## Efficiency

If we only use this API method to reorder, I believe the upper bound for number of API calls to be O(n), where n is the number of tracks in the playlist. This is the case for a playlist in reverse order.

In this repository, I would like to test the effiency for a variety of reordering patterns and playlist sequences. Hopefully, I will be able to find a reasonably efficient reordering method for some common use cases.

### On Reordering by Removal and Addition

Unsurprisingly, it is also possible to add and remove tracks from playlists with the Spotify API. It would also be far more efficient as far as API calls are concerned. If you wanted to sort a reverse-sorted playlist, you could simply remove and then add tracks in the correct order, 100 per API call. Worst case, I believe this would be O(n/50)

However, this method comes with a few downsides. The first is stability. Let's say you sort by removing all tracks and then re-adding them. How do you recover if the program crashes shortly after removing 100+ songs from the playlist? When using the Update endpoint to reorder a playlist, there is no way to accidentally delete or duplicate tracks.  The second downside is that you lose the ability to see the date added. It's nice to be able to sort a playlist to check what songs you added recently. Adding songs via the API method resets that attribute, removing any record of when you personally added the song to the playlist.

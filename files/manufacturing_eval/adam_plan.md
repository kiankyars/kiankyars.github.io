Part description:

A long, slender, brass cylinder, with smaller stepped diameters and threads on both ends. The part is 2 inches long and .187 inches in diameter, so a length:diameter ratio of over 10:1. Chatter / rigidity will be a main concern. On one end of the main diameter, there are two flats, 180 degrees apart. These flats have a small corner radius at both ends, meaning they will have to be cut with the bottom of a radiused end mill. In the flat, there are two threaded holes. It's unclear if they are blind holes or if they go through the part. Due to the thickness of the part, it's likely that they go through to have sufficient thread engagement. On the opposite end of the part, there is a cross hole on the smaller diameter. It is orthogonal to the flats. The cross hole is very close to the shoulder step, so it will be important to watch out for clearance.

Another concern - these small brass threads are very fine and easily damaged. We don't want to clamp on the threads at all or drop the part in any way.

Use coolant for all operations - it probably isn't needed for the lathe ops or drilling the cross hole, but it's reasonable to always use it in enclosed CNC machines, at least for small quantities. If doing a large run, try avoiding coolant use to reduce the need for cleaning parts. There's no need for applying oil when threading the holes - this just contaminates the coolant and coolant will be fine.

Op 1 (Lathe Op):

Get large stock. 0.75 inch diameter is a reasonable choice. This will maintain a ~3:1 L:D ratio, and the single cut to a finished diameter will be taking off ~0.25 inches of radius of material - a large cut, but manageable with a slow feed rate in brass. 0.5 inch could also work. Hold it in a collet, sticking out ~2.25 inches. First, turn / chamfer the smaller diameter and threads, using the existing raw stock for rigidity. Then, turn the main diameter in a single pass, going a bit beyond the end of the part. Use a partoff tool, leaving ~0.020 extra on the opposite end of the part. Don't completely cut the part off - with these small threads, you would be likely to damage the threads if dropping the part, and brass is easily scratched. Leave a ~0.060 diameter when parting off, so you can break the part off of the raw stock by hand.

Op 2 (Lathe Op):

Flip the part around. Use a 0.187 (3/16) collet for concentricity. Control stick out using a reference machined surface - the surface left by the partoff tool is a good bet. Only stick out enough to cut the threads and smaller stepped diameter. Turn the smaller diameter and threads. Blend the smaller diameter into the main diameter using a small chamfer or radius (~0.005 inches).

Op 3 (Mill Op):

I would debate between two options. A collet is a nice option, but I'm a bit concerned about chatter as the stick out would be maybe a 4:1 or 5:1 ratio and the endmill looks like it requires radiused corners, increasing tool pressure. I would probably try this first and see if I can trial and error to get a smooth cut.

If the collet doesn't work, I would try putting the part horizontally in a vise, which is more rigid but could be more fiddly / time consuming to set up. I will give my vise plan below. There is no stick out if holding the part horizontally in a vise, so chatter is less of a concern. It's not ideal to hold a round object in a vise, but we don't have to make major cuts, so we can hold on without a ton of vise pressure which shouldn't scratch the part.

Another concern - how to deburr the threaded holes if they are not blind holes. I think I'll spot drill in the first op, leaving a chamfer, and put the theaded holes in in the second half of this op, so the tap is the last tool used. The threads should be burr free then.

Use a radiused endmill to cut the flat, using multiple small cuts to minimize tool pressure. Use a spot drill to put small chamfers in the flat for the threaded holes - the diameter of the chamfer should be ~0.010 greater than the major diameter of the thread.

Remove the part from the vise and rotate 180 degrees. Index the part by putting the flat down on some sort of reference surface - maybe a step cut into the soft jaws or a gauge block that you use for setup purposes (not for measuring). Cut the second flat. Spot drill / drill / tap the threaded holes. Make sure you have clearance underneath the part for the drill and tap.

You may need to use a bit of scotch brite to debur the flats, but given that the angle between the flats and the diameter isn't very sharp the burr may be minimal.

Op 4 (Mill Op):

Use the vise the grab the flats and place the main diameter down on a reference surface such as parallels or a cut surface in soft jaws. This ensures the part is oriented correctly in all 6 dimensions (rotation and translation). To grab the flats, either cut a small step in some soft jaws, or use something like small gauge blocks between the flat and the vise jaw. Soft jaws would be nice for a higher quantity run, but gauge blocks could be faster for a small quantity run. The gauge block approach would be a bit fiddly when setting up though.

Use a small diameter spot drill with clearance that doesn't hit the large diameter to spot drill the cross hole, then drill the cross hole. Hand debur the opposite side.
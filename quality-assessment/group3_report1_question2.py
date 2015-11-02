"""
Problem 2
finds number of reads in each channel by parsing file names
places channel numbers in dict associated with their number of reads
divides total number of reads with total number of channels for average 
reads per channel
finds channel with greatest number of reads
"""

from glob import glob

passFiles = glob('pass/*.fast5')
failFiles = glob('fail/*.fast5')

channels = {} # making it a dict
numChannels = 0 # track total number of channels
numReads = len(passFiles) + len(failFiles)

for fp in passFiles:    
    fsplit1 = fp.split('\\') # chane to / if not windows
    filename = fsplit1[-1]
    fsplit2 = fp.split('_')
    channelStr = fsplit2[5] # get channel info from file name
    channelNo = int(channelStr[2:]) # get channel number
    if (channelNo in channels) == False: # if this channel has not been encountered before
        numChannels += 1 # add to total number of channels
        channels[channelNo] = 0 # initialize the entry in the dict
    channels[channelNo] += 1 # increment number of files in this channel

for fp in failFiles:    
    fsplit1 = fp.split('\\') # change to / if not windows
    filename = fsplit1[-1]
    fsplit2 = fp.split('_')
    channelStr = fsplit2[5] # get channel info from file name
    channelNo = int(channelStr[2:]) # get channel number
    if (channelNo in channels) == False: # if this channel has not been encountered before
        numChannels += 1 # add to total number of channels
        channels[channelNo] = 0 # initialize the entry in the dict
    channels[channelNo] += 1 # increment number of files in this channel
    
maxChannelNo = max(channels, key=channels.get) # get the key with maximum value associated in the dict
maxChannelCount = channels[maxChannelNo]

#for channel in channels:
#    if channels[channel] > maxChannel:
#        maxChannel = channels[channel]
#        maxChannelNo = channel

avgReadsPerChannel = numReads / numChannels

print("Average reads per channel: " + str(avgReadsPerChannel))
print("Channel with most reads:  " + str(maxChannelNo))
print("Most number of reads: " + str(maxChannelCount))
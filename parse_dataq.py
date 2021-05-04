import os # for file operations

# Parse the DATAQ recorded file created with the DATAQ_BASE class running on linux and return data in dict
# filename: path and file name of the recorded file
# channel_tags: dict that correlate channel with tag name. { 'CH1': 'ASSET.GROUP.TAG1', 'CH2': 'ASSET.GROUP.TAG2' }
#
# return:
#  data: dict [{'tag_name': 'ASSET.GROUP.TAG', 'timestamp':[1234567890,1234567890,...],
#                  'value':[12345.778,12345.75, ...]}]
#
# example of structure of dataq file:
# timestamp: 1619730104324 samplerate: 160000 nchannels: 4
# 1: CH1 0.0141906738 CH2 1.3439941406 CH3 0.0045776367 CH4 -0.0001525879
# 2: CH1 0.0152587891 CH2 -0.2064514160 CH3 0.0061035156 CH4 -0.0001525879

def parse_dataq_file (filename, channel_tag, data):
    # if not os.path.exists(filename+"_lck"):
    #     print(f"The file {filename} lock was not found")
    #     return
    #del_lock_file (filename)

    try:
        f = open(filename, 'r')
        first = True

        for x in f:
            slist = x.split()

            if first:   # check if it is first line
                first = False
                timestamp = int(slist[1])
                #sample_rate = int(slist [3]) # for future use if needed
                nchannels = int(slist[5])

                # prepare data with empty dict but ready to be filled
                # this is based on nchannels
                data = []
                for i in range(nchannels):
                    empty_tag = {'tagName': 'CH'+str(i+1), 'timestamp': [], 'value': []}
                    data.append(empty_tag)

            else:
                #create a dict with the CH1: value1, CH2: value2,...
                for i in range(nchannels):
                    data[i]['timestamp'].append(timestamp)
                    data[i]['value'].append(float(slist[(i+1)*2]))

                #increment timestamp (ms) in 1
                timestamp +=1

        f.close()  # close the file

        # Change the tag name by the actual tag name using the channel_tags cross reference
        for i in range (nchannels):
            ch = 'CH'+str(i+1)  # using for cross reference based on Channel CHX -> real Tag name
            data[i]['tagName'] = channel_tag [ch]

        print(data)
    except Exception as e:
        print(f'[ERROR] Could not open file {filename} or error parsing {e}')



# delete the lock file
def del_lock_file (filename):
    # check for the lock mark
    filename += "_lck"

    if os.path.exists(filename):
        os.remove(filename)
    else:
        print(f"The file {filename} does not exist")

channel = {'CH1': 'TAG1', 'CH2': 'TAG2', 'CH3': 'TAG3', 'CH4': 'TAG4'}
data = dict()

parse_dataq_file('data.txt', channel, data)

import libtorrent
import json
import os

def write_json_file(path, contents):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(contents, f, default=str, indent=4, sort_keys=True)

def parse_torrent_info(info):
    attributes = [
        'name',
        'comment',
        'creator',
        'total_size',
        'piece_length',
        'num_pieces',
        'info_hash',
        'num_files',
        'priv',
        'creation_date',
    ]

    entry = {}

    for attribute in attributes:
        entry[attribute] = getattr(info, attribute, None)()

    return entry

def parse_file_info(file):
    attributes = [
        'path',
        'symlink_path',
        'offset',
        'size',
        'mtime',
        'filehash',
        'pad_file',
        'hidden_attribute',
        'executable_attribute',
        'symlink_attribute',
    ]

    entry = {}

    for attribute in attributes:
        entry[attribute] = getattr(file, attribute, None)

    return entry

def main():
	directory = "./torrents/"
	for filename in os.listdir(directory):
		if filename.endswith(".torrent"): 
			path_to_torrent_file = os.path.join(os.getcwd() + "\\torrents\\", filename) 
			try:
				ti = libtorrent.torrent_info(path_to_torrent_file)
				write_json_file(os.getcwd() + "/json/" + ti.name() + "_torrent_info.json", parse_torrent_info(ti))

				files = []
				for index, file in enumerate(ti.files()):
					files.append(parse_file_info(file))

				write_json_file(os.getcwd() + "/json/" + ti.name() + "_files_info.json", files)		
				#print("JSON Files written for: '" + ti.name() + ".torrent'")	
			except Exception as e:
				print(e)
				continue
		else:
			continue

if __name__ == "__main__":
    main()
    print("Parsing finished successfully.")
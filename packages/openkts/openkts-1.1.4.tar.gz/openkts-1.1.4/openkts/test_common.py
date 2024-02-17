import difflib
import os
import sys
import unittest
from itertools import combinations
import common

'''Unit test function to test the joining of the key shares that have been splitted'''
class TestKeySharesJoin(unittest.TestCase):

    def test_join(self):
        m = 3  # minimum number of shares needed to reconstruct the file
        # List of file shares the file is split into.
        script_directory = os.path.dirname(os.path.abspath(__file__))

        n = [
            os.path.join(script_directory, 'keys', 'Key0.share'),
            os.path.join(script_directory, 'keys', 'Key1.share'),
            os.path.join(script_directory, 'keys', 'Key2.share'),
            os.path.join(script_directory, 'keys', 'Key3.share'),
            os.path.join(script_directory, 'keys', 'Key4.share'),
        ]

        res = list(set(combinations(n, m)))
        # print(f"combinations: {len(res)}")
        # print(f"List of combination: {res}")
        for i, file_shares in enumerate(res):
            output_path = os.path.join(script_directory, 'keys', f"recon_key_combo-{i}.pem")
            original_file_path = os.path.join(script_directory, 'keys', 'Key.pem')
            common.join({'s': list(file_shares), 'd': [], 'o': output_path})
            
            with open(output_path, 'rb') as recon_file, open(original_file_path, 'rb') as original_file:
                recon_content = recon_file.read()
                original_content = original_file.read()

                # if the contents are not the same print the diffences
                if recon_content != original_content:
                    differ = difflib.unified_diff(
                        recon_content.decode('utf-8').splitlines(),
                        original_content.decode('utf-8').splitlines(),
                        lineterm='',
                    )
                    print('\n'.join(differ))
                    
                self.assertEqual(recon_file.read(), original_file.read())
                
                


if __name__ == '__main__':
    unittest.main()
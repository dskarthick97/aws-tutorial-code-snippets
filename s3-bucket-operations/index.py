
from asset_processor import AssetMigration

def process():
    # asset_object = AssetMigration('karthick-leaner-ccp-2021-demo')
    asset_object = AssetMigration('karthick-leaner-ccp-2021-demo', 'private/')
    keys = asset_object.get_keys()
    # keys = asset_object.get_keys(True)
    print(keys)
    
if __name__ == '__main__':
    process()

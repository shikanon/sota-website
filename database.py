#coding:utf-8
import pymongo
import records

class DB:
    def __init__(self):
        self.init_mongo()
        self.init_record()


    def init_mongo(self):
        # mongodb客户端
        mongo_client = pymongo.MongoClient('mongodb://10.10.6.85:27017/')
        api_db = mongo_client["sotaapi"]
        self.api_col = api_db["apiGroup"]
        self.api_col.create_index([('name', pymongo.ASCENDING)], unique=True)


    def init_record(self):
        # 关系型数据库
        self.record_db = records.Database('mysql+pymysql://root:shikanon@10.10.6.85:3306/sota', encoding='utf-8', echo=True)
    

    def create_relation_table(self):
        '''创建数据库'''
        create_index_table = '''CREATE TABLE IF NOT EXISTS sotaindex(
            id int(4) NOT NULL AUTO_INCREMENT,
            name varchar(64) NOT NULL comment '搜索大厅呈现类别',
            APIType int(4) NOT NULL comment '0代表模型接口, 1代表行业解决方案模型, 2 代表数据集接口',
            Image TEXT comment '图片路径',
            PRIMARY KEY ( `id` )
        )DEFAULT CHARSET=utf8 ;
        '''
        create_api_table = '''CREATE TABLE IF NOT EXISTS api(
            id int AUTO_INCREMENT,
            name varchar(255) NOT NULL comment 'API名称',
            APIGroup varchar(32) NOT NULL comment 'API组，属于API种类下的子类，表示一组API的集合',
            APIGroupDescription TEXT,
            DeploymentTime TIMESTAMP comment '部署时间' NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            Description TEXT comment '接口描述',
            APIClass varchar(32) NOT NULL comment 'API种类，如图像生成、人脸识别',
            APIClassDescription TEXT,
            `index_id` int(4) NOT NULL,
            PRIMARY KEY ( `id` ),
            INDEX groupname (APIGroup),
            INDEX classname (APIClass),
            FOREIGN KEY (`index_id`) REFERENCES `sotaindex` (`id`)
        )DEFAULT CHARSET=utf8 ;
        '''
        self.record_db.query(create_index_table)
        self.record_db.query(create_api_table)
    

    def reset(self):
        # 删除关系表
        delete_table = '''DROP TABLE IF EXISTS api'''
        self.record_db.query(delete_table)
        delete_table = '''DROP TABLE IF EXISTS sotaindex'''
        self.record_db.query(delete_table)
        # 删除mongo collections
        self.api_col.remove()
        # 创建表
        self.create_relation_table()
    

    def insert_sotaindex(self, records):
        insert_sql = '''insert ignore into sotaindex(name, APIType, Image)
        values(:name, :APIType, :Image)
        '''
        self.record_db.bulk_query(insert_sql, *records)
    

    def get_sotaindex(self):
        search_sql = "select * from sotaindex;"
        return self.record_db.query(search_sql)
    

    def insert_api(self, records):
        insert_sql = '''
        insert ignore into api (
            name, index_id, APIGroup, APIGroupDescription, APIClass, DeploymentTime, APIClassDescription, Description
        )
        values (
            :name, :index_id, :APIGroup, :APIGroupDescription, :APIClass, :DeploymentTime, :APIClassDescription, :Description
        )
        '''
        self.record_db.bulk_query(insert_sql, *records)
    

    def search_api_from_sotaindex(self, index_id):
        search_sql = "select * from api where index_id=:index_id"
        return self.record_db.query(search_sql,index_id=index_id)


    # def insert_or_update_sdk(self, sdk):
    #     self.api_col.insert_one(sdk)
    
    # def get_sdk(self, name):
    #     self.api_col.find_one(name)


/* 表1注释 */
CREATE TABLE IF NOT EXISTS test1 (
    /* 标题1 */ id INT NOT NULL AUTO_INCREMENT /* 备注1 */,  
    /* 标题2 */ V1 INT DEFAULT 0 /* 备注2 */, 
    PRIMARY KEY (id),
    FOREIGN KEY (V1) REFERENCES test3 (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/* 表2注释(表头说明可缺省) */
CREATE TABLE test2 (
    /* 标题3(标题说明不可缺省) */ id INT NOT NULL AUTO_INCREMENT /* 备注3(备注说明不可缺省) */, 
    /* 标题4 */ V2 ENUM ('7', 'value1', 'value2' ) DEFAULT '7'/* 备注4 */, 
    PRIMARY KEY (id)
);


CREATE TABLE test3 (
    /* 标题5 */ id INT NOT NULL AUTO_INCREMENT /* 备注5 */, 
    /* 标题6 */V3 VARCHAR(900) DEFAULT 'test"+-_*中文string3' /* 备注6 */, 
    /* 标题7 */V3 DATETIME UNIQUE /* 备注7 */, 
    PRIMARY KEY (id)
);
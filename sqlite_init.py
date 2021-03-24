#!/usr/bin/env python
#-*- encoding:utf-8 -*-
import sqlite3

conn = sqlite3.connect('doctor_tools.db')
print("Opened database successfully")
c = conn.cursor()
c.execute(
    '''
    CREATE TABLE IF NOT EXISTS "infusion_schedule"(
        "id" INTEGER PRIMARY KEY AUTOINCREMENT,
        "name" TEXT NOT NULL,
        "start_time" TEXT NOT NULL,
        "end_time" TEXT NOT NULL,
        "interval" INTEGER DEFAULT 0
    );
    '''
)
c.execute(
    '''
    INSERT INTO "infusion_schedule" VALUES (
        3,
        "贾一飞",
        "2021-01-01",
        "2021-12-31",
        5
    )
    '''
)
print("Table created successfully")
conn.commit()
conn.close()
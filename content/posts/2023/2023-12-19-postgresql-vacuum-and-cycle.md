---
title: PostgreSQL Vacuum and Cycle
author: nakji
date: 2023-12-19 17:56:00 +0800
tags: [postgresql vacuum]
showToc: true
TocOpen: true
comments: true
disableHLJS: false
disableShare: false
hideSummary: false
ShowReadingTime: true
ShowBreadCrumbs: true
ShowPostNavLinks: true
ShowWordCount: true
UseHugoToc: true
---

> ** 아래 내용은 GPT4 기반으로 정리했습니다. **

## VACUUM의 목적

1. 저장 공간 회수:    
   PostgreSQL은 MVCC (Multiversion Concurrency Control, 다중 버전 동시성 제어)라는 저장 시스템을 사용합니다.
   이 시스템은 행이 업데이트되거나 삭제될 때마다 새로운 버전의 행을 생성합니다. 이로 인해 오래된 행 버전들이 시간이 지나며 쌓이게 됩니다.
   VACUUM은 이러한 오래되고 불필요한 행 버전을 정리하고 공간을 확보합니다.
2. 트랜잭션 ID Wraparound 방지:    
   PostgreSQL은 트랜잭션을 추적하기 위해 4바이트 트랜잭션 ID를 사용합니다.    
   이 ID는 크기에 제한이 있으며, 결국 wraparound될 수 있습니다.
   이런 상황이 발생하면 데이터베이스는 더 이상 어떤 트랜잭션이 오래되었는지 새로운 것인지를 결정할 수 없게 됩니다.    
   VACUUM은 오래된 트랜잭션 ID를 정리함으로써 이를 방지하는 데 도움이 됩니다.
   
   > Wraparound: 트랜잭션 ID가 그 범위를 초과하여 초기값으로 되돌아가는 현상
3. 쿼리 플래너를 위한 통계 업데이트:    
   VACUUM은 또한 PostgreSQL의 쿼리 플래너에 의해 사용되는 통계를 업데이트하여,    
   데이터베이스가 효율적인 쿼리 실행 계획을 만들 수 있도록 합니다.

## VACUUM의 유형

1. Regular VACUUM:    
   이 과정은 테이블에 락을 걸지 않고 죽은 튜플(오래된 행 버전)을 정리합니다.    
   이는 일상적인 유지 관리 작업입니다.
2. VACUUM FULL:    
   이는 전체 테이블을 새로운 디스크 파일로 다시 write하여, 공간을 압축하고 회수합니다.
   이 작업은 테이블에 락을 걸기 때문에 신중하게 사용해야 합니다.
3. VACUUM ANALYZE:    
   이는 표준 VACUUM 작업을 ANALYZE 명령어와 결합한 것으로, 더 나은 쿼리 계획을 위한 통계를 업데이트합니다.

## 작업 주기

1. 빈도:    
   Vacuum 작업의 빈도는 데이터베이스 작업의 성격에 따라 다릅니다.       
   데이터베이스가 많은 업데이트와 삭제를 겪는 경우, 더 자주 작업을 필요로 할 수 있습니다.
2. Autovacuum을 통한 자동화:    
   PostgreSQL에는 vacuum 과정을 자동화하는 autovacuum 데몬이 포함되어 있습니다.
   데이터베이스 활동에 기반하여 vacuum 빈도를 동적으로 조정하므로 대부분의 데이터베이스에 대해 autovacuum 사용이 권장됩니다.
   
## 고려사항

- 자원 소비:    
  Vacuum 작업은 자원 집약적일 수 있으므로, 가능한 한 활동 시간이 적을 때 스케줄링하는 것이 중요합니다.
- 모니터링:    
  데이터베이스 로그와 성능의 정기적인 모니터링은 필요에 따라 vacuum 작업 스케줄을 조정하는 데 도움이 될 수 있습니다.

    
요약하자면, PostgreSQL에서 VACUUM은 공간을 확보하고, ID wraparound를 방지하며, 쿼리 효율성을 유지하는 데 중요합니다.     
적절한 작업 주기는 데이터베이스 상태에 따라 다르지만, PostgreSQL의 autovacuum 기능은 이 과정을 효과적으로 자동화하도록 설계되었습니다.

## 원문
Purpose of VACUUM:

Reclaims Storage: PostgreSQL uses a storage system known as MVCC (Multiversion Concurrency Control), which creates a new version of a row each time it's updated or deleted. This means that old versions of rows accumulate over time. VACUUM cleans up these old, obsolete row versions and frees up space.
Prevents Transaction ID Wraparound: PostgreSQL uses a 4-byte transaction ID to track transactions. This ID is limited in size and can eventually wrap around. If this happens, the database will no longer be able to determine which transactions are old or new. VACUUM helps prevent this by cleaning up old transaction IDs.
Updates Statistics for the Query Planner: VACUUM also updates the statistics used by PostgreSQL's query planner, ensuring that the database can create efficient query execution plans.
Types of VACUUM:

Regular VACUUM: This process cleans up dead tuples (old versions of rows) without locking the table. It's a routine maintenance task.
VACUUM FULL: This rewrites the entire table to a new disk file, compacting it and reclaiming disk space. This operation locks the table, so it should be used cautiously.
VACUUM ANALYZE: This combines the standard VACUUM operation with an ANALYZE command, which updates statistics for better query planning.
Work Cycle:

Frequency: The frequency of vacuuming depends on the nature of your database operations. If your database undergoes a lot of updates and deletions, more frequent vacuuming might be necessary.
Automation with Autovacuum: PostgreSQL includes an autovacuum daemon that automates the vacuuming process. It's recommended to use autovacuum for most databases because it dynamically adjusts the frequency of vacuuming based on database activity.
Considerations:

Resource Consumption: Vacuuming can be resource-intensive, so it's important to schedule it during periods of low activity if possible.
Monitoring: Regular monitoring of database logs and performance can help you adjust the vacuuming schedule as needed.
In summary, VACUUM in PostgreSQL is crucial for reclaiming space, preventing ID wraparound, and maintaining query efficiency. The appropriate work cycle varies based on database activity, but the autovacuum feature in PostgreSQL is designed to automate this process effectively.

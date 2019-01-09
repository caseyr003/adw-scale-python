/* 
Sample Workloads for initial data in ADW 
These can be used to force the database to scale 
Credit:
    http://oracledatagroup.com
*/


-- Query 1
SELECT sum(lo_extendedprice*lo_discount/1000/1000) as revenue
from ssb.lineorder, ssb.dwdate
where lo_orderdate = d_datekey
and d_yearmonthnum = 199401
and lo_discount between 4 and 6
and lo_quantity between 26 and 35;

-- Query 2
SELECT count(*) from 
(
select sum(lo_revenue), d_year, p_brand1
from ssb.lineorder, ssb.dwdate, ssb.part, ssb.supplier
where lo_orderdate = d_datekey
and lo_partkey = p_partkey
and lo_suppkey = s_suppkey
and p_category = 'MFGR#12'
and s_region = 'AMERICA'
group by d_year, p_brand1
order by d_year, p_brand1
);

-- Query 3
SELECT count(*) from 
(
select c_nation, s_nation, d_year, sum(lo_revenue) as revenue
from ssb.customer, ssb.lineorder, ssb.supplier, ssb.dwdate
where lo_custkey = c_custkey
and lo_suppkey = s_suppkey
and lo_orderdate = d_datekey
and c_region = 'ASIA' and s_region = 'ASIA'
and d_year >= 1992 and d_year <= 1997
group by c_nation, s_nation, d_year
order by d_year asc, revenue desc
);

-- Query 4
SELECT count(*) from 
(
select d_year, s_nation, p_category, sum(lo_revenue - lo_supplycost) as profit
from ssb.dwdate, ssb.customer, ssb.supplier, ssb.part, ssb.lineorder
where lo_custkey = c_custkey
and lo_suppkey = s_suppkey
and lo_partkey = p_partkey
and lo_orderdate = d_datekey
and c_region = 'AMERICA'
and s_region = 'AMERICA'
and (d_year = 1997 or d_year = 1998)
and (p_mfgr = 'MFGR#1'
or p_mfgr = 'MFGR#2')
group by d_year, s_nation, p_category
order by d_year, s_nation, p_category
);

-- Analytic View Query 1
SELECT count(*) from 
(
SELECT
dwdate_hier.member_name as year,
part_hier.member_name as part,
customer_hier.c_region,
customer_hier.member_name as customer,
lo_quantity,
lo_revenue
FROM ssb.ssb_av
HIERARCHIES (
dwdate_hier,
part_hier,
customer_hier)
WHERE
dwdate_hier.d_year = '1998'
AND dwdate_hier.level_name = 'MONTH'
AND part_hier.level_name = 'MANUFACTURER'
AND customer_hier.c_region = 'AMERICA'
AND customer_hier.level_name = 'NATION'
ORDER BY
dwdate_hier.hier_order,
part_hier.hier_order,
customer_hier.hier_order
);

-- Analytic View Query 2
SELECT count(*) from 
(
SELECT
dwdate_hier.member_name as year,
part_hier.member_name as part,
customer_hier.member_name as customer,
supplier_hier.member_name as supplier,
lo_quantity,
lo_revenue,
lo_supplycost
FROM ssb.ssb_av
HIERARCHIES (
dwdate_hier,
part_hier,
customer_hier,
supplier_hier)
WHERE
dwdate_hier.d_yearmonth = 'Apr1998'
AND dwdate_hier.level_name = 'DAY'
AND part_hier.level_name = 'MANUFACTURER'
AND customer_hier.c_region = 'AMERICA'
AND customer_hier.c_nation = 'CANADA'
AND customer_hier.level_name = 'CITY'
AND supplier_hier.level_name = 'REGION'
ORDER BY
dwdate_hier.hier_order,
part_hier.hier_order,
customer_hier.hier_order,
supplier_hier.hier_order
);

pg_dump cricket-tales2 > /tmp/ctbak.psql
gzip -c /tmp/ctbak.psql | uuencode ctbak.psql.gz  | mail -s "cricket tales backup" nebogeo@gmail.com


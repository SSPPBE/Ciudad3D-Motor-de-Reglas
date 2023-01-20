--create database epok;

CREATE EXTENSION postgis;

INSERT INTO spatial_ref_sys (srid,auth_name,auth_srid,srtext,proj4text) VALUES
	 (97433,'sr-org',7433,'PROJCS["GKBA",GEOGCS["International 1909 (Hayford)",DATUM["CAI",SPHEROID["intl",6378388,297]],PRIMEM["Greenwich",0],UNIT["degree",0.0174532925199433]],PROJECTION["Transverse_Mercator"],PARAMETER["latitude_of_origin",-34.629269],PARAMETER["central_meridian",-58.463300],PARAMETER["scale_factor",0.999998],PARAMETER["false_easting",100000],PARAMETER["false_northing",100000],UNIT["Meter",1]]','+proj=tmerc +lat_0=-34.629269 +lon_0=-58.4633 +k=0.9999980000000001 +x_0=100000 +y_0=100000 +ellps=intl +units=m +no_defs ');


-- public.cur3d_areaproteccionhistorica definition

-- Drop table

-- DROP TABLE public.cur3d_areaproteccionhistorica;

CREATE TABLE public.cur3d_areaproteccionhistorica (
	id serial4 NOT NULL,
	barrios varchar(18) NULL,
	comuna int4 NULL,
	s_m_p varchar(254) NULL,
	smp varchar(254) NULL,
	"1_calle" varchar(254) NULL,
	"1_altura" varchar(254) NULL,
	"1_direccio" varchar(254) NULL,
	"2_calle" varchar(254) NULL,
	"2_alt" varchar(254) NULL,
	"2_direccio" varchar(254) NULL,
	"3_calle" varchar(254) NULL,
	"3_alt" varchar(254) NULL,
	"3_direccio" varchar(254) NULL,
	"4_calle" varchar(254) NULL,
	"4_alt" varchar(254) NULL,
	"4_direccio" varchar(254) NULL,
	denominaci varchar(254) NULL,
	catalogaci varchar(254) NULL,
	aph_nro_y_ varchar(254) NULL,
	proteccion varchar(254) NULL,
	estado varchar(254) NULL,
	ley_3056 varchar(254) NULL,
	timestamp_alta timestamptz NULL,
	timestamp_modificacion timestamptz NULL,
	observaciones_publicables text NULL,
	observaciones_privadas text NULL,
	publicable bool NOT NULL,
	verificado bool NOT NULL,
	geom public.geometry(multipolygon, 97433) NULL,
	CONSTRAINT cur3d_areaproteccionhistorica_pkey PRIMARY KEY (id)
);
CREATE INDEX cur3d_areap_smp_7dcc15_idx ON public.cur3d_areaproteccionhistorica USING btree (smp);
CREATE INDEX cur3d_areaproteccionhistorica_geom_id ON public.cur3d_areaproteccionhistorica USING gist (geom);


-- public.cur3d_manzana definition

-- Drop table

-- DROP TABLE public.cur3d_manzana;

CREATE TABLE public.cur3d_manzana (
	id serial4 NOT NULL,
	sm varchar(10) NULL,
	tipo varchar(255) NULL,
	fuente varchar(25) NULL,
	timestamp_alta timestamptz NULL,
	timestamp_modificacion timestamptz NULL,
	observaciones_publicables text NULL,
	observaciones_privadas text NULL,
	publicable bool NOT NULL,
	verificado bool NOT NULL,
	geom public.geometry(multipolygon, 97433) NULL,
	CONSTRAINT cur3d_manzana_pkey PRIMARY KEY (id)
);
CREATE INDEX cur3d_manza_sm_c78959_idx ON public.cur3d_manzana USING btree (sm);
CREATE INDEX cur3d_manzana_geom_id ON public.cur3d_manzana USING gist (geom);


-- public.cur3d_manzanaatipica definition

-- Drop table

-- DROP TABLE public.cur3d_manzanaatipica;

CREATE TABLE public.cur3d_manzanaatipica (
	id serial4 NOT NULL,
	manzana varchar(5) NOT NULL,
	seccion varchar(5) NOT NULL,
	sm varchar(11) NOT NULL,
	nivel varchar(5) NULL,
	mz_tipo varchar(10) NULL,
	cant_lados int4 NULL,
	mz_sup float8 NULL,
	cant_pa int4 NULL,
	area_esp varchar(30) NULL,
	uni_edif varchar(4) NULL,
	oferta varchar(2) NULL,
	obras varchar(2) NULL,
	superficie varchar(50) NULL,
	trazado varchar(2) NULL,
	disposicio varchar(255) NULL,
	parc_catal varchar(3) NULL,
	cant_parce varchar(3) NULL,
	timestamp_alta timestamptz NOT NULL,
	timestamp_modificacion timestamptz NOT NULL,
	observaciones_publicables text NOT NULL,
	observaciones_privadas text NOT NULL,
	publicable bool NOT NULL,
	verificado bool NOT NULL,
	the_geom public.geometry(multipolygon, 97433) NULL,
	pdf varchar(255) NULL,
	CONSTRAINT cur3d_manzanaatipica_pkey PRIMARY KEY (id)
);
CREATE INDEX cur3d_manza_sm_d1494f_idx ON public.cur3d_manzanaatipica USING btree (sm);
CREATE INDEX cur3d_manzanaatipica_the_geom_id ON public.cur3d_manzanaatipica USING gist (the_geom);


-- public.cur3d_parcela definition

-- Drop table

-- DROP TABLE public.cur3d_parcela;

CREATE TABLE public.cur3d_parcela (
	id serial4 NOT NULL,
	smp varchar(15) NULL,
	fuente varchar(25) NULL,
	area float8 NULL,
	geom public.geometry(multipolygon, 97433) NULL,
	observaciones_privadas text NULL,
	observaciones_publicables text NULL,
	publicable bool NOT NULL,
	timestamp_alta timestamptz NULL,
	timestamp_modificacion timestamptz NULL,
	verificado bool NOT NULL,
	CONSTRAINT cur3d_parcela_pkey PRIMARY KEY (id)
);
CREATE INDEX cur3d_parce_smp_c68e2d_idx ON public.cur3d_parcela USING btree (smp);


-- public.cur3d_superficieedificableplanta definition

-- Drop table

-- DROP TABLE public.cur3d_superficieedificableplanta;

CREATE TABLE public.cur3d_superficieedificableplanta (
	id serial4 NOT NULL,
	smp varchar(16) NULL,
	fuente varchar(25) NULL,
	observaciones_privadas text NULL,
	observaciones_publicables text NULL,
	publicable bool NOT NULL,
	superficie float8 NULL,
	timestamp_alta timestamptz NULL,
	timestamp_modificacion timestamptz NULL,
	verificado bool NOT NULL,
	CONSTRAINT cur3d_superficieedificableplanta_pkey PRIMARY KEY (id)
);
CREATE INDEX cur3d_super_smp_04c355_idx ON public.cur3d_superficieedificableplanta USING btree (smp);


-- public.mindesarrollourbanoytransporte_codigourbanistico definition

-- Drop table

-- DROP TABLE public.mindesarrollourbanoytransporte_codigourbanistico;

CREATE TABLE public.mindesarrollourbanoytransporte_codigourbanistico (
	id serial4 NOT NULL,
	smp1 varchar(255) NOT NULL,
	uni_edif_1 float8 NULL,
	uni_edif_2 float8 NULL,
	uni_edif_3 float8 NULL,
	uni_edif_4 float8 NULL,
	uso_1 int4 NULL,
	uso_2 int4 NULL,
	uso_3 int4 NULL,
	dist_1_grp varchar(50) NULL,
	dist_1_esp varchar(50) NULL,
	dist_2_grp varchar(50) NULL,
	dist_2_esp varchar(50) NULL,
	dist_3_grp varchar(50) NULL,
	dist_3_esp varchar(50) NULL,
	dist_4_grp varchar(50) NULL,
	dist_4_esp varchar(50) NULL,
	anac int4 NULL,
	ci_digital int4 NOT NULL,
	rh int4 NOT NULL,
	lep int4 NOT NULL,
	ensanche int4 NOT NULL,
	apertura int4 NOT NULL,
	catalogado int4 NOT NULL,
	rivolta int4 NOT NULL,
	incid_uva float8 NULL,
	alicuota float8 NOT NULL,
	dist_cpu_1 varchar(50) NULL,
	dist_cpu_2 varchar(50) NULL,
	barrio varchar(25) NOT NULL,
	comuna varchar(15) NOT NULL,
	timestamp_alta timestamptz NOT NULL,
	timestamp_modificacion timestamptz NOT NULL,
	observaciones_publicables text NOT NULL,
	observaciones_privadas text NOT NULL,
	publicable bool NOT NULL,
	verificado bool NOT NULL,
	the_geom public.geometry(multipolygon, 97433) NULL,
	fot_em_1 float8 NULL,
	plano_l float8 NULL,
	manzana varchar(254) NULL,
	parcela varchar(254) NULL,
	seccion varchar(254) NULL,
	cpu_obsv varchar(255) NULL,
	fot_em_2 float8 NULL,
	fot_pl_1 float8 NULL,
	fot_pl_2 float8 NULL,
	fot_sl_1 float8 NULL,
	fot_sl_2 float8 NULL,
	plano_l_ob varchar(255) NULL,
	tipo_mza varchar(255) NULL,
	ae_fot_bas float8 NULL,
	zona_1 varchar(100) NULL,
	zona_2 varchar(100) NULL,
	irregular bool NULL,
	adps varchar(255) NULL,
	memo varchar(255) NULL,
	microcentr varchar(255) NULL,
	CONSTRAINT mindesarrollourbanoytransporte_codigourbanistico_pkey PRIMARY KEY (id)
);
CREATE INDEX mindesarrol_smp1_af00eb_idx ON public.mindesarrollourbanoytransporte_codigourbanistico USING btree (smp1);
CREATE INDEX mindesarrollourbanoytransporte_codigourbanistico_the_geom_id ON public.mindesarrollourbanoytransporte_codigourbanistico USING gist (the_geom);

create schema algoritmo;

-- algoritmo.manzana definition

-- Drop table

-- DROP TABLE algoritmo.manzana;

CREATE TABLE algoritmo.manzana (
	sm varchar(10) NULL,
	tipo varchar(255) NULL,
	seccion varchar(5) NULL,
	manzana varchar(5) NULL,
	nivel varchar(5) NULL,
	cant_lados int4 NULL,
	mz_sup float8 NULL,
	cant_pa int4 NULL,
	area_esp varchar(30) NULL,
	uni_edif varchar(4) NULL,
	oferta varchar(2) NULL,
	obras varchar(2) NULL,
	superficie varchar(50) NULL,
	trazado varchar(2) NULL,
	disposicio varchar(255) NULL,
	parc_catal varchar(3) NULL,
	cant_parce varchar(3) NULL,
	pdf varchar(255) NULL,
	geom public.geometry NULL
);


-- algoritmo.parcela definition

-- Drop table

-- DROP TABLE algoritmo.parcela;

CREATE TABLE algoritmo.parcela (
	smp varchar(15) NULL,
	sm varchar(50) NULL,
	area float8 NULL,
	area_parcela float8 NULL,
	barrios varchar(18) NULL,
	comuna int4 NULL,
	"1_calle" varchar(254) NULL,
	"1_altura" varchar(254) NULL,
	"1_direccio" varchar(254) NULL,
	"2_calle" varchar(254) NULL,
	"2_alt" varchar(254) NULL,
	"2_direccio" varchar(254) NULL,
	"3_calle" varchar(254) NULL,
	"3_alt" varchar(254) NULL,
	"3_direccio" varchar(254) NULL,
	"4_calle" varchar(254) NULL,
	"4_alt" varchar(254) NULL,
	"4_direccio" varchar(254) NULL,
	denominaci varchar(254) NULL,
	catalogaci varchar(254) NULL,
	aph_nro_y_ varchar(254) NULL,
	proteccion varchar(254) NULL,
	estado varchar(254) NULL,
	ley_3056 varchar(254) NULL,
	uni_edif_1 numeric NULL,
	uni_edif_2 numeric NULL,
	uni_edif_3 numeric NULL,
	uni_edif_4 numeric NULL,
	uso_1 int8 NULL,
	uso_2 int8 NULL,
	uso_3 int8 NULL,
	dist_1_grp varchar(50) NULL,
	dist_1_esp varchar(50) NULL,
	dist_2_grp varchar(50) NULL,
	dist_2_esp varchar(50) NULL,
	dist_3_grp varchar(50) NULL,
	dist_3_esp varchar(50) NULL,
	dist_4_grp varchar(50) NULL,
	dist_4_esp varchar(50) NULL,
	anac int4 NULL,
	ci_digital int4 NULL,
	rh int4 NULL,
	lep int4 NULL,
	ensanche int4 NULL,
	apertura int4 NULL,
	catalogado int4 NULL,
	rivolta int4 NULL,
	incid_uva float8 NULL,
	alicuota float8 NULL,
	dist_cpu_1 varchar(50) NULL,
	dist_cpu_2 varchar(50) NULL,
	fot_em_1 float8 NULL,
	plano_l float8 NULL,
	manzana varchar(254) NULL,
	parcela varchar(254) NULL,
	seccion varchar(254) NULL,
	cpu_obsv varchar(255) NULL,
	fot_em_2 float8 NULL,
	fot_pl_1 float8 NULL,
	fot_pl_2 float8 NULL,
	fot_sl_1 float8 NULL,
	fot_sl_2 float8 NULL,
	plano_l_ob varchar(255) NULL,
	tipo_mza varchar(255) NULL,
	ae_fot_bas float8 NULL,
	zona_1 varchar(100) NULL,
	zona_2 varchar(100) NULL,
	irregular bool NULL,
	enrase bool NULL,
	geom public.geometry NULL
);

CREATE OR REPLACE FUNCTION algoritmo.actualizarciudad3d_2()
 RETURNS integer
 LANGUAGE plpgsql
AS $function$
begin
delete from public.cur3d_manzana;

INSERT INTO public.cur3d_manzana (sm, tipo, geom, timestamp_alta, timestamp_modificacion, observaciones_publicables, observaciones_privadas, publicable,verificado, fuente)	  
(SELECT sm, tipo, ST_SetSRID(geom, 97433), localtimestamp, localtimestamp, '', '', true,true, 'ALGORITMO' FROM algoritmo.manzana);

-- cur3d_manzanaatipica
-- ERROR DE NOMBRE: ES TODO
----------------------------------
--truncate table public.cur3d_manzanaatipica restart identity;
delete from public.cur3d_manzanaatipica;

INSERT INTO public.cur3d_manzanaatipica (
	manzana, seccion, sm, nivel, mz_tipo, cant_lados, mz_sup, cant_pa, area_esp,
	uni_edif, oferta, obras, superficie, trazado, disposicio, parc_catal, cant_parce, pdf, 
  the_geom,
	timestamp_alta, timestamp_modificacion, observaciones_publicables, observaciones_privadas,publicable,verificado)
SELECT 
	manzana, seccion, sm, nivel, tipo, cant_lados, mz_sup, cant_pa, area_esp,
	uni_edif, oferta, obras, superficie, trazado, disposicio, parc_catal, cant_parce, pdf, 
	ST_SetSRID(geom, 97433),
  localtimestamp, localtimestamp,'', 	'',  true,true 	
FROM algoritmo.manzana;

----------------------------------
-- parcela
----------------------------------

--truncate table public.cur3d_parcela restart identity;
delete from public.cur3d_parcela;

INSERT INTO public.cur3d_parcela ( 
    smp, area, 
	   geom, 
    timestamp_alta, timestamp_modificacion, observaciones_publicables, observaciones_privadas, publicable, verificado, fuente)
SELECT 
	  smp, area_parcela, 
	  ST_SetSRID(geom, 97433),
      localtimestamp, localtimestamp, '', '', true, true, 'ALGORITMO'
FROM algoritmo.parcela;

--VA ------------------------------
--cur3d_superficieedificableplanta -> Lo que tengo en el primer insumo de la edificabilidad
-- calculo dissolve de volumenes, calculo de area
----------------------------------
--truncate table public.cur3d_superficieedificableplanta restart identity;
delete from public.mindesarrollourbanoytransporte_codigourbanistico;

update algoritmo.parcela set barrios = '' where barrios is null;
INSERT INTO public.mindesarrollourbanoytransporte_codigourbanistico 
( smp1,uni_edif_1,uni_edif_2,uni_edif_3,uni_edif_4,uso_1,uso_2,uso_3,dist_1_grp,dist_1_esp,dist_2_grp,dist_2_esp,dist_3_grp,dist_3_esp,dist_4_grp,dist_4_esp,
  anac,ci_digital,rh,lep,ensanche,apertura,catalogado,rivolta,incid_uva,alicuota,dist_cpu_1,dist_cpu_2,
  barrio,comuna,fot_em_1,plano_l,manzana,parcela,seccion,cpu_obsv,fot_em_2,fot_pl_1,fot_pl_2,fot_sl_1,fot_sl_2,plano_l_ob,tipo_mza,ae_fot_bas,zona_1,zona_2,
  irregular,adps,memo,microcentr,the_geom,timestamp_alta,timestamp_modificacion,observaciones_publicables,observaciones_privadas,publicable,verificado)  
select smp,uni_edif_1,uni_edif_2,uni_edif_3,uni_edif_4,uso_1,uso_2,uso_3,dist_1_grp,dist_1_esp,dist_2_grp,dist_2_esp,dist_3_grp,dist_3_esp,dist_4_grp,dist_4_esp,
  anac,ci_digital,rh,lep,ensanche,apertura,catalogado,rivolta,incid_uva,alicuota,dist_cpu_1,dist_cpu_2,
  barrios,comuna,fot_em_1,plano_l,manzana,parcela,seccion,cpu_obsv,fot_em_2,fot_pl_1,fot_pl_2,fot_sl_1,fot_sl_2,plano_l_ob,tipo_mza,ae_fot_bas,zona_1,zona_2,
  irregular,adps,memo,microcentr,
  ST_SetSRID(geom, 97433),
  localtimestamp, localtimestamp, '', '', true, true
 from algoritmo.parcela;
----------------------------------
-- cur3d_areaproteccionhistorica
----------------------------------
--truncate table public.cur3d_areaproteccionhistorica restart identity;
delete from public.cur3d_areaproteccionhistorica;

INSERT INTO public.cur3d_areaproteccionhistorica (
	barrios, comuna, s_m_p , smp, "1_calle", "1_altura", "1_direccio", "2_calle", "2_alt", "2_direccio",
	"3_calle", "3_alt", "3_direccio", "4_calle", "4_alt", "4_direccio", denominaci, catalogaci, "aph_nro_y_",
	proteccion, estado, ley_3056,
	geom, 
	timestamp_alta, timestamp_modificacion, observaciones_publicables, observaciones_privadas, publicable,verificado)	
SELECT 
	  barrios, comuna, smp , smp, "1_calle", "1_altura", "1_direccio", "2_calle", "2_alt", "2_direccio",
	  "3_calle", "3_alt", "3_direccio", "4_calle", "4_alt", "4_direccio", denominaci, catalogaci, 
	  aph_nro_y_, proteccion, estado, ley_3056, 
	  ST_SetSRID(geom, 97433),
	  localtimestamp, localtimestamp, '', '', true,true 
FROM algoritmo.parcela;

--VA ------------------------------
--cur3d_superficieedificableplanta -> Lo que tengo en el primer insumo de la edificabilidad
-- calculo dissolve de volumenes, calculo de area
----------------------------------
--truncate table public.cur3d_superficieedificableplanta restart identity;
delete from public.cur3d_superficieedificableplanta;

INSERT INTO public.cur3d_superficieedificableplanta (
       smp, superficie, 
	   fuente, timestamp_alta, timestamp_modificacion, observaciones_publicables, observaciones_privadas, publicable, verificado)
SELECT smp, area, 
	  'ALGORITMO', localtimestamp, localtimestamp, '', '', true, true
FROM algoritmo.parcela;

   ---
   return 0;
   ---
END;
$function$
;
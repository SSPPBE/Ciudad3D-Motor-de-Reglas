--create database pdi;

CREATE EXTENSION postgis;

INSERT INTO spatial_ref_sys (srid,auth_name,auth_srid,srtext,proj4text) VALUES
	 (97433,'sr-org',7433,'PROJCS["GKBA",GEOGCS["International 1909 (Hayford)",DATUM["CAI",SPHEROID["intl",6378388,297]],PRIMEM["Greenwich",0],UNIT["degree",0.0174532925199433]],PROJECTION["Transverse_Mercator"],PARAMETER["latitude_of_origin",-34.629269],PARAMETER["central_meridian",-58.463300],PARAMETER["scale_factor",0.999998],PARAMETER["false_easting",100000],PARAMETER["false_northing",100000],UNIT["Meter",1]]','+proj=tmerc +lat_0=-34.629269 +lon_0=-58.4633 +k=0.9999980000000001 +x_0=100000 +y_0=100000 +ellps=intl +units=m +no_defs ');


-- public.aph_ssregic definition

-- Drop table

-- DROP TABLE aph_ssregic;

CREATE TABLE aph_ssregic (
	gid serial4 NOT NULL,
	barrios varchar(18) NULL,
	comuna int4 NULL,
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
	the_geom public.geometry NULL,
	CONSTRAINT aph_ssregic_pkey PRIMARY KEY (gid)
);


-- public.cur_ae26 definition

-- Drop table

-- DROP TABLE cur_ae26;

CREATE TABLE cur_ae26 (
	"CALLE" varchar(255) NULL,
	"DESDE" varchar(255) NULL,
	"HASTA" varchar(255) NULL,
	"SUBGRUPO" varchar(255) NULL,
	"UNIDADEDIFICABILIDAD" varchar(255) NULL
);


-- public.cur_callejero definition

-- Drop table

-- DROP TABLE cur_callejero;

CREATE TABLE cur_callejero (
	gid serial4 NOT NULL,
	id int4 NULL,
	codigo int4 NULL,
	nomoficial varchar(254) NULL,
	alt_izqini int4 NULL,
	alt_izqfin int4 NULL,
	alt_derini int4 NULL,
	alt_derfin int4 NULL,
	nomanter varchar(254) NULL,
	nom_mapa varchar(254) NULL,
	tipo_c varchar(254) NULL,
	long numeric NULL,
	sentido varchar(254) NULL,
	cod_sent int4 NULL,
	observa varchar(254) NULL,
	bicisenda varchar(254) NULL,
	lado_ciclo varchar(254) NULL,
	recorrid_x varchar(254) NULL,
	ciclo_obse varchar(254) NULL,
	tooltip_bi varchar(254) NULL,
	red_jerarq varchar(60) NULL,
	red_tp varchar(16) NULL,
	ffcc varchar(30) NULL,
	tipo_ffcc varchar(150) NULL,
	comuna int4 NULL,
	com_par int4 NULL,
	com_impar int4 NULL,
	barrio varchar(50) NULL,
	barrio_par varchar(50) NULL,
	barrio_imp varchar(50) NULL,
	the_geom public.geometry NULL,
	CONSTRAINT cur_callejero_pkey PRIMARY KEY (gid)
);


-- public.cur_consolidados definition

-- Drop table

-- DROP TABLE cur_consolidados;

CREATE TABLE cur_consolidados (
	gid serial4 NOT NULL,
	smp varchar(254) NULL,
	sm varchar(254) NULL,
	consol_txt varchar(254) NULL,
	porc_cons float8 NULL,
	the_geom public.geometry NULL,
	CONSTRAINT cur_consolidados_pkey PRIMARY KEY (gid)
);
CREATE INDEX sidx_cur_consolidados_the_geom ON public.cur_consolidados USING gist (the_geom);


-- public.cur_lfi_particularizadas definition

-- Drop table

-- DROP TABLE cur_lfi_particularizadas;

CREATE TABLE cur_lfi_particularizadas (
	gid serial4 NOT NULL,
	manzana varchar(254) NULL,
	seccion varchar(254) NULL,
	mz_tipo varchar(254) NULL,
	sm varchar(254) NULL,
	disposicio varchar(254) NULL,
	the_geom public.geometry NULL,
	CONSTRAINT cur_lfi_particularizadas_pkey PRIMARY KEY (gid)
);


-- public.cur_lib_particularizadas definition

-- Drop table

-- DROP TABLE cur_lib_particularizadas;

CREATE TABLE cur_lib_particularizadas (
	gid serial4 NOT NULL,
	manzana varchar(254) NULL,
	seccion varchar(254) NULL,
	mz_tipo varchar(254) NULL,
	sm varchar(254) NULL,
	disposicio varchar(254) NULL,
	the_geom public.geometry NULL,
	CONSTRAINT cur_lib_particularizadas_pkey PRIMARY KEY (gid)
);


-- public.cur_lineasparcelas definition

-- Drop table

-- DROP TABLE cur_lineasparcelas;

CREATE TABLE cur_lineasparcelas (
	gid serial4 NOT NULL,
	smp varchar(254) NULL,
	tipo varchar(254) NULL,
	the_geom public.geometry NULL,
	CONSTRAINT cur_lineasparcelas_pkey PRIMARY KEY (gid)
);


-- public.cur_manzanasatipicas definition

-- Drop table

-- DROP TABLE cur_manzanasatipicas;

CREATE TABLE cur_manzanasatipicas (
	gid serial4 NOT NULL,
	fid numeric NULL,
	cat numeric NULL,
	featid1 numeric NULL,
	manzana varchar(254) NULL,
	seccion varchar(254) NULL,
	nivel varchar(254) NULL,
	obs varchar(254) NULL,
	origen varchar(254) NULL,
	mz_tipo varchar(254) NULL,
	cant_lados numeric NULL,
	mz_sup numeric NULL,
	cant_pa numeric NULL,
	lfi varchar(254) NULL,
	lib varchar(254) NULL,
	sm varchar(254) NULL,
	comuna varchar(254) NULL,
	area_esp varchar(254) NULL,
	uni_edif varchar(254) NULL,
	oferta varchar(254) NULL,
	obras varchar(254) NULL,
	superficie varchar(254) NULL,
	trazado varchar(254) NULL,
	disposicio varchar(254) NULL,
	parc_catal varchar(254) NULL,
	cant_parce varchar(254) NULL,
	the_geom public.geometry NULL,
	pdf varchar(254) NULL,
	CONSTRAINT cur_manzanasatipicas_pkey PRIMARY KEY (gid)
);


-- public.cur_parcelas definition

-- Drop table

-- DROP TABLE cur_parcelas;

CREATE TABLE cur_parcelas (
	gid serial4 NOT NULL,
	smp varchar(254) NULL,
	seccion varchar(254) NULL,
	manzana varchar(254) NULL,
	parcela varchar(254) NULL,
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
	zona_1 varchar(50) NULL,
	zona_2 varchar(50) NULL,
	anac int8 NULL,
	ci_digital int8 NULL,
	rh int8 NULL,
	lep int8 NULL,
	ensanche int8 NULL,
	apertura int8 NULL,
	catalogado int8 NULL,
	tipo_mza varchar(50) NULL,
	rivolta int8 NULL,
	barrio varchar(50) NULL,
	comuna varchar(50) NULL,
	plano_l numeric NULL,
	plano_l_ob varchar(100) NULL,
	dist_cpu_1 varchar(50) NULL,
	dist_cpu_2 varchar(50) NULL,
	fot_em_1 numeric NULL,
	fot_em_2 numeric NULL,
	fot_pl_1 numeric NULL,
	fot_pl_2 numeric NULL,
	fot_sl_1 numeric NULL,
	fot_sl_2 numeric NULL,
	cpu_base varchar(50) NULL,
	ae_fot_bas numeric NULL,
	cpu_obs varchar(100) NULL,
	alicuota numeric NULL,
	inc_uva_21 int4 NULL,
	sm varchar(50) NULL,
	the_geom public.geometry NULL,
	adps varchar(255) NULL,
	memo varchar(255) NULL,
	microcentr varchar(255) NULL,
	CONSTRAINT cur_parcelas_pkey2 PRIMARY KEY (gid)
);


-- public.cur_restricciones definition

-- Drop table

-- DROP TABLE cur_restricciones;

CREATE TABLE cur_restricciones (
	gid serial4 NOT NULL,
	tipo varchar(254) NULL,
	nro_ord varchar(254) NULL,
	obs varchar(254) NULL,
	the_geom public.geometry NULL,
	CONSTRAINT cur_restricciones_pkey PRIMARY KEY (gid)
);


-- public.cur_riesgo_arqueologico definition

-- Drop table

-- DROP TABLE cur_riesgo_arqueologico;

CREATE TABLE cur_riesgo_arqueologico (
	gid serial4 NOT NULL,
	tipo varchar(254) NULL,
	the_geom public.geometry NULL,
	CONSTRAINT cur_riesgo_arquelogico_pkey PRIMARY KEY (gid)
);


-- public.cur_riesgohidrico definition

-- Drop table

-- DROP TABLE cur_riesgohidrico;

CREATE TABLE cur_riesgohidrico (
	gid serial4 NOT NULL,
	riesgo_hid varchar(254) NULL,
	the_geom public.geometry NULL,
	CONSTRAINT cur_riesgohidrico_pkey PRIMARY KEY (gid)
);


-- public.cur_secciones definition

-- Drop table

-- DROP TABLE cur_secciones;

CREATE TABLE cur_secciones (
	gid serial4 NOT NULL,
	rot_sec varchar(16) NULL,
	seccion varchar(16) NULL,
	superficie numeric NULL,
	the_geom public.geometry NULL,
	CONSTRAINT cur_secciones_pkey PRIMARY KEY (gid)
);


-- public.cur_tejido definition

-- Drop table

-- DROP TABLE cur_tejido;

CREATE TABLE cur_tejido (
	gid serial4 NOT NULL,
	featid1 int8 NULL,
	objectid int8 NULL,
	tag varchar(254) NULL,
	sec varchar(254) NULL,
	man varchar(254) NULL,
	par varchar(254) NULL,
	area numeric NULL,
	len int8 NULL,
	bajos int8 NULL,
	altos int8 NULL,
	flagtipo varchar(254) NULL,
	lay varchar(254) NULL,
	sm varchar(254) NULL,
	smp varchar(254) NULL,
	alt_2013 numeric NULL,
	piso_2013 int8 NULL,
	observacio varchar(254) NULL,
	actualizac varchar(254) NULL,
	smp_2013 varchar(254) NULL,
	alt_ant numeric NULL,
	alt_extr numeric NULL,
	alt_2017 numeric NULL,
	piso_2017 int8 NULL,
	smp_2017 varchar(254) NULL,
	ant_2017 float8 NULL,
	extr_2017 float8 NULL,
	agip varchar(50) NULL,
	the_geom public.geometry NULL,
	CONSTRAINT cur_tejido_pkey PRIMARY KEY (gid)
);
CREATE INDEX sidx_cur_tejido_the_geom ON public.cur_tejido USING gist (the_geom);


-- public.cur_volumenes_particularizados definition

-- Drop table

-- DROP TABLE cur_volumenes_particularizados;

CREATE TABLE cur_volumenes_particularizados (
	gid serial4 NOT NULL,
	id int8 NULL,
	smp varchar(19) NULL,
	tipo varchar(20) NULL,
	altura_ini numeric NULL,
	altura_fin numeric NULL,
	fuente varchar(25) NULL,
	edificabil varchar(254) NULL,
	the_geom public.geometry NULL,
	CONSTRAINT cur_volumenes_particularizados_pkey PRIMARY KEY (gid)
);


-- public.frentesparcelas definition

-- Drop table

-- DROP TABLE frentesparcelas;

CREATE TABLE frentesparcelas (
	gid serial4 NOT NULL,
	anio_act varchar(254) NULL,
	clase varchar(254) NULL,
	dato_orige varchar(254) NULL,
	fecha varchar(254) NULL,
	frente varchar(254) NULL,
	featid1 float8 NULL,
	lad_mens varchar(254) NULL,
	lindero varchar(254) NULL,
	manzana varchar(254) NULL,
	mh varchar(254) NULL,
	num_dom varchar(254) NULL,
	ochava varchar(254) NULL,
	parcela varchar(254) NULL,
	parc_esq varchar(254) NULL,
	particular varchar(254) NULL,
	seccion varchar(254) NULL,
	smp varchar(254) NULL,
	sup varchar(254) NULL,
	the_geom public.geometry NULL,
	CONSTRAINT frentesparcelas_pkey PRIMARY KEY (gid)
);
CREATE INDEX frentesparcelas_idx_smp ON public.frentesparcelas USING btree (smp);
CREATE INDEX frentesparcelasidxfrentenum ON public.frentesparcelas USING btree (frente, num_dom);
CREATE INDEX sidx_mo_frentesparcelas_the_geom ON public.frentesparcelas USING gist (the_geom);


-- public.mo_manzanasmap definition

-- Drop table

-- DROP TABLE mo_manzanasmap;

CREATE TABLE mo_manzanasmap (
	gid serial4 NOT NULL,
	fid numeric NULL,
	cat numeric(10) NULL,
	featid1 numeric(10) NULL,
	manzana varchar(254) NULL,
	seccion varchar(254) NULL,
	nivel varchar(254) NULL,
	obs varchar(254) NULL,
	origen varchar(254) NULL,
	mz_tipo varchar(254) NULL,
	cant_lados numeric(10) NULL,
	mz_sup numeric NULL,
	cant_pa numeric(10) NULL,
	lfi varchar(254) NULL,
	lib varchar(254) NULL,
	sm varchar(254) NULL,
	the_geom public.geometry NULL,
	CONSTRAINT mo_manzanasmap_pkey1 PRIMARY KEY (gid)
);
CREATE INDEX sidx_mo_manzanasmap_the_geom ON public.mo_manzanasmap USING gist (the_geom);


-- public.mo_parcelasmap definition

-- Drop table

-- DROP TABLE mo_parcelasmap;

CREATE TABLE mo_parcelasmap (
	gid serial4 NOT NULL,
	fid_1 int4 NULL,
	featid1 float8 NULL,
	manzana varchar(254) NULL,
	obs varchar(254) NULL,
	parcela varchar(254) NULL,
	seccion varchar(254) NULL,
	smp varchar(254) NULL,
	partida varchar(254) NULL,
	sup_edif varchar(254) NULL,
	unidades varchar(254) NULL,
	fid_2 int4 NULL,
	barrios varchar(18) NULL,
	comuna int2 NULL,
	area float8 NULL,
	perimeter float8 NULL,
	acres float8 NULL,
	dist_m2 numeric NULL,
	hectares float8 NULL,
	the_geom public.geometry NULL,
	CONSTRAINT mo_parcelasmap_pkey PRIMARY KEY (gid)
);
CREATE INDEX mo_parcelasmapw0 ON public.mo_parcelasmap USING btree (smp);
CREATE INDEX mo_parcelasmapwl ON public.mo_parcelasmap USING btree (smp);
CREATE INDEX sidx_mo_parcelasmap_the_geom ON public.mo_parcelasmap USING gist (the_geom);

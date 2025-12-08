--
-- PostgreSQL database dump
--

\restrict 2Abnihha3RfBnBnwXpbBQ9tJYxalARDrpkROpb3QasevdIZFbwqRNcHusXS0JU2

-- Dumped from database version 14.20 (Homebrew)
-- Dumped by pg_dump version 14.20 (Homebrew)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: certificados; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.certificados (
    id integer NOT NULL,
    docente_id integer NOT NULL,
    codigo_unico character varying(14) NOT NULL,
    hash_verificacion character varying(128) NOT NULL,
    qr_path character varying(255),
    fecha_generacion timestamp without time zone,
    fecha_ultima_actualizacion timestamp without time zone,
    valido boolean,
    docente_criterio_id integer,
    codigo_emi character varying(50)
);


--
-- Name: certificados_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.certificados_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: certificados_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.certificados_id_seq OWNED BY public.certificados.id;


--
-- Name: docentes; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.docentes (
    id integer NOT NULL,
    nombres character varying(100) NOT NULL,
    apellidos character varying(100) NOT NULL,
    ci character varying(20),
    unidad_academica_id integer,
    cargo character varying(150),
    "años_servicio" integer,
    email character varying(120),
    telefono character varying(20),
    foto character varying(255),
    requiere_regeneracion boolean,
    fecha_registro timestamp without time zone,
    fecha_actualizacion timestamp without time zone,
    activo boolean
);


--
-- Name: docentes_criterios; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.docentes_criterios (
    id integer NOT NULL,
    docente_id integer NOT NULL,
    tipo_criterio_id integer NOT NULL,
    detalles text NOT NULL,
    fecha_registro timestamp without time zone,
    fecha_actualizacion timestamp without time zone
);


--
-- Name: docentes_criterios_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.docentes_criterios_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: docentes_criterios_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.docentes_criterios_id_seq OWNED BY public.docentes_criterios.id;


--
-- Name: docentes_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.docentes_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: docentes_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.docentes_id_seq OWNED BY public.docentes.id;


--
-- Name: tipos_criterios; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.tipos_criterios (
    id integer NOT NULL,
    nombre character varying(300) NOT NULL,
    descripcion text,
    orden integer,
    activo boolean,
    fecha_creacion timestamp without time zone
);


--
-- Name: tipos_criterios_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.tipos_criterios_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: tipos_criterios_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.tipos_criterios_id_seq OWNED BY public.tipos_criterios.id;


--
-- Name: unidades_academicas; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.unidades_academicas (
    id integer NOT NULL,
    codigo character varying(10) NOT NULL,
    nombre character varying(200) NOT NULL,
    ciudad character varying(100) NOT NULL,
    activo boolean,
    fecha_creacion timestamp without time zone
);


--
-- Name: unidades_academicas_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.unidades_academicas_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: unidades_academicas_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.unidades_academicas_id_seq OWNED BY public.unidades_academicas.id;


--
-- Name: usuarios; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.usuarios (
    id integer NOT NULL,
    username character varying(80) NOT NULL,
    password_hash character varying(255) NOT NULL,
    nombre_completo character varying(200),
    email character varying(120),
    fecha_creacion timestamp without time zone,
    activo boolean
);


--
-- Name: usuarios_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.usuarios_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: usuarios_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.usuarios_id_seq OWNED BY public.usuarios.id;


--
-- Name: certificados id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.certificados ALTER COLUMN id SET DEFAULT nextval('public.certificados_id_seq'::regclass);


--
-- Name: docentes id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.docentes ALTER COLUMN id SET DEFAULT nextval('public.docentes_id_seq'::regclass);


--
-- Name: docentes_criterios id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.docentes_criterios ALTER COLUMN id SET DEFAULT nextval('public.docentes_criterios_id_seq'::regclass);


--
-- Name: tipos_criterios id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tipos_criterios ALTER COLUMN id SET DEFAULT nextval('public.tipos_criterios_id_seq'::regclass);


--
-- Name: unidades_academicas id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.unidades_academicas ALTER COLUMN id SET DEFAULT nextval('public.unidades_academicas_id_seq'::regclass);


--
-- Name: usuarios id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.usuarios ALTER COLUMN id SET DEFAULT nextval('public.usuarios_id_seq'::regclass);


--
-- Data for Name: certificados; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.certificados (id, docente_id, codigo_unico, hash_verificacion, qr_path, fecha_generacion, fecha_ultima_actualizacion, valido, docente_criterio_id, codigo_emi) FROM stdin;
3	2	70E5-DC53-1D59	b6c3a47f02dd6b2b80791f2f09a33dc5413854aa4683592db4b6a767ed341da3	/Users/alvaroencinas/Desktop/sistema_de_certificacion_docentes/app/static/qr_codes/70E5-DC53-1D59.png	2025-12-08 16:45:43.857621	2025-12-08 16:45:43.857628	t	3	EMI-DNICYT-CERT.00001/2025
4	2	057C-9455-F547	871b0d155a12cfb7c768ac1621f381cdc228f3d68115d85c628d878334a54684	/Users/alvaroencinas/Desktop/sistema_de_certificacion_docentes/app/static/qr_codes/057C-9455-F547.png	2025-12-08 16:45:43.885427	2025-12-08 16:45:43.885431	t	4	EMI-DNICYT-CERT.00002/2025
5	5	FCC0-23F5-2EC9	5a3ea6b20432d8733f954f6468e00980b82869b0a2e7521e985b8141374de1d9	/Users/alvaroencinas/Desktop/sistema_de_certificacion_docentes/app/static/qr_codes/FCC0-23F5-2EC9.png	2025-12-08 16:54:45.610831	2025-12-08 16:54:45.610842	t	5	EMI-DNICYT-CERT.00003/2025
6	6	3DF6-3404-C4BF	c46d05d5d43da11dff699076b45c19a35728b984e6f8726e41a0e72ee22d4b0e	/Users/alvaroencinas/Desktop/sistema_de_certificacion_docentes/app/static/qr_codes/3DF6-3404-C4BF.png	2025-12-08 17:03:32.412974	2025-12-08 17:03:32.412979	t	6	EMI-DNICYT-CERT.00004/2025
7	8	62F6-ACCA-38CC	6394bc51e3076955bd2cfea5066fcbc254ba79c2b7ff3fa3d213532886f1b10e	/Users/alvaroencinas/Desktop/sistema_de_certificacion_docentes/app/static/qr_codes/62F6-ACCA-38CC.png	2025-12-08 18:07:10.654996	2025-12-08 18:07:10.655005	t	7	EMI-DNICYT-CERT.00005/2025
8	9	EF79-E8E1-4FC4	3fbeabad3b735c6d41dec835dc3f6c80728001151c23a3151c1aabe57d12a82c	/Users/alvaroencinas/Desktop/sistema_de_certificacion_docentes/app/static/qr_codes/EF79-E8E1-4FC4.png	2025-12-08 18:12:05.480201	2025-12-08 18:12:05.480209	t	8	EMI-DNICYT-CERT.00006/2025
10	11	6723-27E5-AFE6	c351c1a13b91e634956edda4b94df169baacf9abc143345eb51aa4ce2a2aa0a0	/Users/alvaroencinas/Desktop/sistema_de_certificacion_docentes/app/static/qr_codes/6723-27E5-AFE6.png	2025-12-08 18:18:21.412141	2025-12-08 18:18:21.412148	t	10	EMI-DNICYT-CERT.00007/2025
11	12	D549-7319-4651	fbc99581021c4c5252533a9acca7eb34e5c50b74037a58f1624fca72e09de95c	/Users/alvaroencinas/Desktop/sistema_de_certificacion_docentes/app/static/qr_codes/D549-7319-4651.png	2025-12-08 18:19:41.926145	2025-12-08 18:19:41.926155	t	11	EMI-DNICYT-CERT.00008/2025
\.


--
-- Data for Name: docentes; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.docentes (id, nombres, apellidos, ci, unidad_academica_id, cargo, "años_servicio", email, telefono, foto, requiere_regeneracion, fecha_registro, fecha_actualizacion, activo) FROM stdin;
11	Natalia	Lozano	\N	\N	\N	\N	\N	\N	\N	t	2025-12-08 18:18:11.200489	2025-12-08 18:18:11.200501	t
12	Carlos	Pacheco	\N	\N	\N	\N	\N	\N	\N	t	2025-12-08 18:19:24.774315	2025-12-08 18:19:24.774323	t
1	Ing. Alvaro Santiago	Encinas Flores	13493105	1	Docente - Ing. de Sistemas	5	aencinasf@est.emi.edu.bo	76260216	\N	f	2025-12-05 23:07:15.817442	2025-12-06 02:38:32.689134	t
2	Ing. Edwin Rodrigo	Alaro Fernandez	1234567	1	Encargado de Laboratorio	4	ealarof@doc.emi.edu.bo	+59162843994	\N	f	2025-12-06 03:27:43.620983	2025-12-06 03:29:07.980701	t
4	Ing. Claudia Daniela	Nina Castillo	\N	\N	\N	\N	\N	\N	\N	t	2025-12-08 16:27:16.568366	2025-12-08 16:27:16.568374	t
5	Claudia Daniela	Nina Castillo	\N	\N	\N	\N	\N	\N	\N	t	2025-12-08 16:54:23.380061	2025-12-08 16:54:23.380067	t
6	LIC. WILFREDO	HEREDIA DELIAS	\N	\N	\N	\N	\N	\N	\N	t	2025-12-08 17:03:09.115742	2025-12-08 17:03:09.115753	t
7	Lic. Alan	Huanca Mamani	\N	\N	\N	\N	\N	\N	\N	t	2025-12-08 17:14:29.320252	2025-12-08 17:14:29.32026	t
8	Marco	Antonio	\N	\N	\N	\N	\N	\N	\N	t	2025-12-08 18:06:50.476511	2025-12-08 18:06:50.476518	t
9	Luis	Sanchez	\N	\N	\N	\N	\N	\N	\N	t	2025-12-08 18:11:52.422017	2025-12-08 18:11:52.422025	t
10	Luis	Sanchez	\N	\N	\N	\N	\N	\N	\N	t	2025-12-08 18:12:45.821133	2025-12-08 18:12:45.821137	t
\.


--
-- Data for Name: docentes_criterios; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.docentes_criterios (id, docente_id, tipo_criterio_id, detalles, fecha_registro, fecha_actualizacion) FROM stdin;
1	1	2	- Congreso de IA	2025-12-05 23:08:09.836012	2025-12-05 23:08:09.836019
2	1	5	- Simposio Nacional de Tecnología	2025-12-05 23:08:09.841359	2025-12-05 23:08:09.841365
3	2	2	- Taller de IA	2025-12-06 03:28:52.934092	2025-12-06 03:28:52.934102
4	2	9	- Congreso Nacional de Ingeniería	2025-12-06 03:28:52.939729	2025-12-06 03:28:52.939736
5	5	1	- Taller de IA 2025	2025-12-08 16:54:42.151947	2025-12-08 16:54:42.15196
6	6	1	- GUÍA DE EJERCICIOS “ESTADÍSTICA I”, componente Práctica, asignatura Estadística I, Ciencias Básicas, Carreras Tecnológicas; fecha de edición: 11 de febrero de 2025.	2025-12-08 17:03:29.23851	2025-12-08 17:03:29.23852
7	8	2	- Curso	2025-12-08 18:07:07.817515	2025-12-08 18:07:07.817522
8	9	1	- curso de hackeo	2025-12-08 18:12:02.454947	2025-12-08 18:12:02.454959
9	10	4	- Curso	2025-12-08 18:12:55.103334	2025-12-08 18:12:55.103343
10	11	2	Congreso de IA	2025-12-08 18:18:20.002856	2025-12-08 18:18:20.00287
11	12	8	_ REvisfjidofjsoifj_ REvisfjidofjsoifj_ REvisfjidofjsoifj_ REvisfjidofjsoifj_ REvisfjidofjsoifj_ REvisfjidofjsoifj_ REvisfjidofjsoifj_ REvisfjidofjsoifj_ REvisfjidofjsoifj_ REvisfjidofjsoifj_ REvisfjidofjsoifj_ REvisfjidofjsoifj_ REvisfjidofjsoifj	2025-12-08 18:19:39.957169	2025-12-08 18:19:39.957178
\.


--
-- Data for Name: tipos_criterios; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.tipos_criterios (id, nombre, descripcion, orden, activo, fecha_creacion) FROM stdin;
1	TALLERES Y CONGRESOS, SIMPOSIOS O SEMINARIOS COMO PONENTE - EMI	\N	1	t	2025-12-05 23:05:04.189816
2	TALLERES Y CONGRESOS, SIMPOSIOS O SEMINARIOS COMO PONENTE	\N	2	t	2025-12-05 23:05:04.191194
3	TEXTOS ACADÉMICOS, GUÍAS, MANUALES, VIDEOS EDUCATIVOS - EMI	\N	3	t	2025-12-05 23:05:04.191954
4	TEXTOS ACADÉMICOS, GUÍAS, MANUALES, VIDEOS EDUCATIVOS	\N	4	t	2025-12-05 23:05:04.192658
5	LIBROS (SENAPI o ISBN) - EMI	\N	5	t	2025-12-05 23:05:04.193464
6	LIBROS (SENAPI o ISBN)	\N	6	t	2025-12-05 23:05:04.194044
7	ARTÍCULOS ACADÉMICOS (OPINIÓN, REFLEXIÓN, REV. BIBLIOGRÁFICA) - EMI	\N	7	t	2025-12-05 23:05:04.194613
8	ARTÍCULOS ACADÉMICOS (OPINIÓN, REFLEXIÓN, REV. BIBLIOGRÁFICA)	\N	8	t	2025-12-05 23:05:04.195163
9	ARTÍCULOS CIENTÍFICOS INDEXADOS (QS) - EMI	\N	9	t	2025-12-05 23:05:04.195756
10	ARTÍCULOS CIENTÍFICOS INDEXADOS (QS)	\N	10	t	2025-12-05 23:05:04.196337
\.


--
-- Data for Name: unidades_academicas; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.unidades_academicas (id, codigo, nombre, ciudad, activo, fecha_creacion) FROM stdin;
1	UALP	Unidad Académica La Paz	La Paz	t	2025-12-05 23:05:04.182641
2	UACB	Unidad Académica Cochabamba	Cochabamba	t	2025-12-05 23:05:04.185285
3	UASC	Unidad Académica Santa Cruz	Santa Cruz	t	2025-12-05 23:05:04.185932
4	UARB	Unidad Académica Riberalta	Riberalta	t	2025-12-05 23:05:04.18661
5	UATP	Unidad Académica Trópico	Trópico	t	2025-12-05 23:05:04.187459
\.


--
-- Data for Name: usuarios; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.usuarios (id, username, password_hash, nombre_completo, email, fecha_creacion, activo) FROM stdin;
1	admin	scrypt:32768:8:1$kHqaohJD5bYOwOa7$870ff0b956ceb9452947e2534544f4c620775dc9315eb7b8f83b713727ca2df9c9d63307970d112fdc1ce2646d33b10a8b5511e19c44c30ed0cbf0e3d6050cb5	Administrador	admin@emi.edu.bo	2025-12-05 23:05:43.642519	t
\.


--
-- Name: certificados_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.certificados_id_seq', 11, true);


--
-- Name: docentes_criterios_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.docentes_criterios_id_seq', 11, true);


--
-- Name: docentes_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.docentes_id_seq', 12, true);


--
-- Name: tipos_criterios_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.tipos_criterios_id_seq', 10, true);


--
-- Name: unidades_academicas_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.unidades_academicas_id_seq', 5, true);


--
-- Name: usuarios_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.usuarios_id_seq', 1, true);


--
-- Name: certificados certificados_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.certificados
    ADD CONSTRAINT certificados_pkey PRIMARY KEY (id);


--
-- Name: docentes_criterios docentes_criterios_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.docentes_criterios
    ADD CONSTRAINT docentes_criterios_pkey PRIMARY KEY (id);


--
-- Name: docentes docentes_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.docentes
    ADD CONSTRAINT docentes_pkey PRIMARY KEY (id);


--
-- Name: tipos_criterios tipos_criterios_nombre_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tipos_criterios
    ADD CONSTRAINT tipos_criterios_nombre_key UNIQUE (nombre);


--
-- Name: tipos_criterios tipos_criterios_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tipos_criterios
    ADD CONSTRAINT tipos_criterios_pkey PRIMARY KEY (id);


--
-- Name: unidades_academicas unidades_academicas_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.unidades_academicas
    ADD CONSTRAINT unidades_academicas_pkey PRIMARY KEY (id);


--
-- Name: certificados uq_certificados_codigo_emi; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.certificados
    ADD CONSTRAINT uq_certificados_codigo_emi UNIQUE (codigo_emi);


--
-- Name: certificados uq_certificados_docente_criterio; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.certificados
    ADD CONSTRAINT uq_certificados_docente_criterio UNIQUE (docente_criterio_id);


--
-- Name: docentes_criterios uq_docente_criterio; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.docentes_criterios
    ADD CONSTRAINT uq_docente_criterio UNIQUE (docente_id, tipo_criterio_id);


--
-- Name: usuarios usuarios_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.usuarios
    ADD CONSTRAINT usuarios_pkey PRIMARY KEY (id);


--
-- Name: ix_certificados_codigo_unico; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX ix_certificados_codigo_unico ON public.certificados USING btree (codigo_unico);


--
-- Name: ix_docentes_ci; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX ix_docentes_ci ON public.docentes USING btree (ci);


--
-- Name: ix_unidades_academicas_codigo; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX ix_unidades_academicas_codigo ON public.unidades_academicas USING btree (codigo);


--
-- Name: ix_usuarios_username; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX ix_usuarios_username ON public.usuarios USING btree (username);


--
-- Name: certificados certificados_docente_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.certificados
    ADD CONSTRAINT certificados_docente_id_fkey FOREIGN KEY (docente_id) REFERENCES public.docentes(id);


--
-- Name: docentes_criterios docentes_criterios_docente_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.docentes_criterios
    ADD CONSTRAINT docentes_criterios_docente_id_fkey FOREIGN KEY (docente_id) REFERENCES public.docentes(id);


--
-- Name: docentes_criterios docentes_criterios_tipo_criterio_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.docentes_criterios
    ADD CONSTRAINT docentes_criterios_tipo_criterio_id_fkey FOREIGN KEY (tipo_criterio_id) REFERENCES public.tipos_criterios(id);


--
-- Name: docentes docentes_unidad_academica_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.docentes
    ADD CONSTRAINT docentes_unidad_academica_id_fkey FOREIGN KEY (unidad_academica_id) REFERENCES public.unidades_academicas(id);


--
-- Name: certificados fk_certificados_docente_criterio; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.certificados
    ADD CONSTRAINT fk_certificados_docente_criterio FOREIGN KEY (docente_criterio_id) REFERENCES public.docentes_criterios(id) ON DELETE CASCADE;


--
-- PostgreSQL database dump complete
--

\unrestrict 2Abnihha3RfBnBnwXpbBQ9tJYxalARDrpkROpb3QasevdIZFbwqRNcHusXS0JU2


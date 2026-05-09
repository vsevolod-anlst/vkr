--
-- PostgreSQL database dump
--

\restrict sw9f5c2rvHNBMBjIVu3DWrwJ7owyg526kGetqbwdxgtG9eXwXzJLw0rm8BhBpaZ

-- Dumped from database version 15.17 (Debian 15.17-1.pgdg13+1)
-- Dumped by pg_dump version 15.17 (Debian 15.17-1.pgdg13+1)

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
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


ALTER TABLE public.alembic_version OWNER TO postgres;

--
-- Name: query_logs; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.query_logs (
    id integer NOT NULL,
    question text NOT NULL,
    answer text NOT NULL,
    generation_time double precision,
    created_at timestamp without time zone
);


ALTER TABLE public.query_logs OWNER TO postgres;

--
-- Name: query_logs_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.query_logs_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.query_logs_id_seq OWNER TO postgres;

--
-- Name: query_logs_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.query_logs_id_seq OWNED BY public.query_logs.id;


--
-- Name: query_logs id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.query_logs ALTER COLUMN id SET DEFAULT nextval('public.query_logs_id_seq'::regclass);


--
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.alembic_version (version_num) FROM stdin;
7f6a5ec725a9
\.


--
-- Data for Name: query_logs; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.query_logs (id, question, answer, generation_time, created_at) FROM stdin;
\.


--
-- Name: query_logs_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.query_logs_id_seq', 1, false);


--
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- Name: query_logs query_logs_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.query_logs
    ADD CONSTRAINT query_logs_pkey PRIMARY KEY (id);


--
-- Name: ix_query_logs_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_query_logs_id ON public.query_logs USING btree (id);


--
-- PostgreSQL database dump complete
--

\unrestrict sw9f5c2rvHNBMBjIVu3DWrwJ7owyg526kGetqbwdxgtG9eXwXzJLw0rm8BhBpaZ


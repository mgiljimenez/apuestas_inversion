-- Imputar los valores iniciales

INSERT INTO cuentas (descripcion)
VALUES ('Cuenta_Banco_Central'),
('Cuenta_Beneficios'),
('1xbet_casa'),
('1xbet_apostado'),
('William Hill_casa'),
('William Hill_apostado'),
('Betsson_casa'),
('Betsson_apostado'),
('Gran Casino Madrid_casa'),
('Gran Casino Madrid_apostado'),
('Interwetten_casa'),
('Interwetten_apostado'),
('Luckia_casa'),
('Luckia_apostado'),
('Marathon Bet_casa'),
('Marathon Bet_apostado'),
('Bwin_casa'),
('Bwin_apostado'),
('Sportium_casa'),
('Sportium_apostado'),
('Codere_casa'),
('Codere_apostado'),
('Winamax_casa'),
('Winamax_apostado'),
('Zebet_casa'),
('Zebet_apostado'),
('Bet365_casa'),
('Bet365_apostado'),
('MiguelGJ_inversor'),
('JulioGN_inversor');


INSERT INTO casas_apuesta (nombre, descripcion, url, id_cuenta_casa, id_cuenta_apostado)
VALUES ('1xbet', 'Descripción', 'https://1xbet.es/', 3, 4),
('William Hill', 'Descripción', 'https://sports.williamhill.es/betting/es-es', 5, 6),
('Betsson', 'Descripción', 'https://www.betsson.es/apuestas-deportivas/', 7, 8),
('Gran Casino Madrid', 'Descripción', 'https://www.casinogranmadridonline.es/apuestas-deportivas', 9, 10),
('Interwetten', 'Descripción', 'https://www.interwetten.es/es/apuestas-deportivas', 11, 12),
('Luckia', 'Descripción', 'https://www.luckia.es/apuestas/', 13, 14),
('Marathon Bet', 'Descripción', 'https://www.marathonbet.es/es?cppcids=all', 15, 16),
('Bwin', 'Descripción', 'https://sports.bwin.es/es/sports', 17, 18),
('Sportium', 'Descripción', 'https://www.sportium.es/apuestas-deportivas', 19, 20),
('Codere', 'Descripción', 'https://www.codere.es/', 21, 22),
('Winamax', 'Descripción', 'https://www.winamax.es/', 23, 24),
('Zebet', 'Descripción', 'https://www.zebet.es/', 25, 26),
('Bet365', 'Descripción', 'https://www.bet365.es/', 27, 28);

INSERT INTO inversores (nombre, fecha_registro, id_cuenta)
VALUES ('Miguel Gil Jimenez', '2023-05-01', 29),
('Julio Gil Navarro', '2023-05-01', 30);

INSERT INTO deportes (deporte)
VALUES ('Tenis'),
('Baloncesto');
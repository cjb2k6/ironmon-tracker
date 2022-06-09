timeLimit = 30
diff = 0

game='gold'

view='lead'

attack_ivs = {'2', '3', '6', '7', 'a', 'e', 'f'}
attack_ivs_length = 7

NAME_LENGTH = 10

TEAM_SIZE_ADDR = tonumber("0x1A22")

POKE_ENEMY_ID_ADDR = tonumber("0x10ED")
POKE_ENEMY_LEVEL_ADDR = tonumber("0x10FC")
POKE_ENEMY_IV_ADDR = tonumber("0x10F5")
POKE_ENEMY_TYPE_ADDR = tonumber("0x110D")

POKE_1_NAME_ADDR = tonumber("0x1B8C")
POKE_1_ID_ADDR = tonumber("0x1A23")
POKE_1_LEVEL_ADDR = tonumber("0x1A49")

GOT_STARTER_ADDR = tonumber("0x1986")

ITEM_OFFSET = 8
MOVE_OFFSET = 9
PP_OFFSET = 30

MAIL_ADDR = tonumber("0x0600")
IGNORE_MAIL = "0"
WRITE_MAIL = "1"
READ_MAIL = "2"
SAVE_MAIL = "3"

BATTLE_TYPE = tonumber("0x1116")

GAME_ADDR = tonumber("0x013C")
SILVER = 83
GOLD = 71
CRYSTAL = 65

TYPES = {
   [0] = 'Normal',
   [1] = 'Fighting',
   [2] = 'Flying',
   [3] = 'Poison',
   [4] = 'Ground',
   [5] = 'Rock',
   [6] = 'Bug',
   [7] = 'Ghost',
   [8] = 'Steel',
   [20] =  'Fire',
   [21] = 'Water',
   [22] = 'Grass',
   [23] =  'Electric',
   [24] = 'Psychic',
   [25] = 'Ice',
   [26] = 'Dragon',
   [27] = 'Dark'
}

function loadCrystalAddresses()
    TEAM_SIZE_ADDR = tonumber("0x1CD7")
    POKE_1_NAME_ADDR = tonumber("0x1E41")
    POKE_1_ID_ADDR = tonumber("0x1CDF")
    POKE_1_LEVEL_ADDR = tonumber("0x1CFE")

    POKE_ENEMY_ID_ADDR = tonumber("0x1204")
    POKE_ENEMY_LEVEL_ADDR = tonumber("0x1213")
    POKE_ENEMY_IV_ADDR = tonumber("0x120C")
    POKE_ENEMY_TYPE_ADDR = tonumber("0x1224")

    BATTLE_TYPE = tonumber("0x122D")

    ITEM_OFFSET = 1
    MOVE_OFFSET = 2
    PP_OFFSET = 23
end

function getPokeName(startAddress)
	name = "["
	index = 0

	while index < NAME_LENGTH do
		name = name .. memory.readbyte(startAddress + index)
		if index ~= (NAME_LENGTH - 1) then
			name = name .. ", "
		end
		index = index + 1
	end

	return name .. "]"
end

function getIsShiny(lvlAddr)
    ad_iv = string.format("%x", memory.readbyte(lvlAddr - 10))
    ss_iv = string.format("%x", memory.readbyte(lvlAddr - 9))
    attack = string.sub(ad_iv, 0, 1)
    defense = string.sub(ad_iv, 2, 2)
    speed = string.sub(ss_iv, 0, 1)
    special = string.sub(ss_iv, 2, 2)

    if speed == 'a' and defense == 'a' and special == 'a' then
        for i = 0,attack_ivs_length,1
        do
           if attack == attack_ivs[i] then
            return 1
           end
        end
    end
    return 0
end

function getPP(pp)
    pp_val = tonumber(pp)
    if pp_val > 192 then
        pp_val = pp_val - 192
    elseif pp_val > 128 then
        pp_val = pp_val - 128
    elseif pp_val > 64 then
        pp_val = pp_val - 64
    end
    return pp_val
end

function getEnemyTypes()
    type1code = memory.readbyte(POKE_ENEMY_TYPE_ADDR)
    type2code = memory.readbyte(POKE_ENEMY_TYPE_ADDR + 1)

    if type1code == type2code then
        return '"' .. TYPES[type1code] .. '"'
    else
        return '"' .. TYPES[type1code] .. '", "' .. TYPES[type2code] .. '"'
    end
end

function mail()
    memory.usememorydomain("CartRAM")
    bytes = {}

    file = io.open("mail", "r")

    contents = file:read "*a"

    io.close(file)

    tokens = string.gmatch(contents, "([^,]+)")

    output = ""
    operation = IGNORE_MAIL

    i = 0
    for token in tokens do
        if i == 0 then
            if token == IGNORE_MAIL or token == SAVE_MAIL then
                return
            else
                operation = token
            end
        end

        if operation == WRITE_MAIL then
            -- Write Mail to CartRAM
            if i > 0 then
                output = output .. ','
                memory.writebyte(MAIL_ADDR + i - 1, tonumber(token))
                output = output .. token
            else
                output = output .. IGNORE_MAIL
                print('Overwriting mail')
            end
         elseif operation == READ_MAIL then
            -- Read Mail from CartRAM
            if i > 0 then
                output = output .. ','
                output = output .. memory.readbyte(MAIL_ADDR + i - 1)
            else
                output = output .. SAVE_MAIL
                print('Reading mail')
            end
        end
        i = i + 1
    end

    file = io.open("mail", "w")

    io.output(file)

    io.write(output)
    io.close(file)
end


function buildPoke(number, nameAddr, idAddr, lvlAddr)
 poke = "\"poke" .. number .. "\": {"
 poke = poke .. "\"name\": " .. getPokeName(nameAddr) .. ", "
 poke = poke .. "\"id\": \"" .. memory.readbyte(idAddr) .. "\"" .. ", "
 poke = poke .. "\"item\": \"" .. memory.readbyte(idAddr + ITEM_OFFSET) .. "\"" .. ", "
 poke = poke .. "\"move_1\": \"" .. memory.readbyte(idAddr + MOVE_OFFSET) .. "\"" .. ", "
 poke = poke .. "\"move_2\": \"" .. memory.readbyte(idAddr + MOVE_OFFSET + 1) .. "\"" .. ", "
 poke = poke .. "\"move_3\": \"" .. memory.readbyte(idAddr  + MOVE_OFFSET + 2) .. "\"" .. ", "
 poke = poke .. "\"move_4\": \"" .. memory.readbyte(idAddr + MOVE_OFFSET + 3) .. "\"" .. ", "
 poke = poke .. "\"pp_1\": \"" .. getPP(memory.readbyte(idAddr + PP_OFFSET)) .. "\"" .. ", "
 poke = poke .. "\"pp_2\": \"" .. getPP(memory.readbyte(idAddr + PP_OFFSET + 1)) .. "\"" .. ", "
 poke = poke .. "\"pp_3\": \"" .. getPP(memory.readbyte(idAddr + PP_OFFSET + 2)) .. "\"" .. ", "
 poke = poke .. "\"pp_4\": \"" .. getPP(memory.readbyte(idAddr + PP_OFFSET + 3)) .. "\"" .. ", "
 poke = poke .. "\"level\": " .. memory.readbyte(lvlAddr) .. ", "
 poke = poke .. "\"hp\": " .. memory.read_u16_be(lvlAddr + 3) .. ", "
 poke = poke .. "\"max_hp\": " .. memory.read_u16_be(lvlAddr + 5) .. ", "
 poke = poke .. "\"attack\": " .. memory.read_u16_be(lvlAddr + 7) .. ", "
 poke = poke .. "\"defense\": " .. memory.read_u16_be(lvlAddr + 9) .. ", "
 poke = poke .. "\"speed\": " .. memory.read_u16_be(lvlAddr + 11) .. ", "
 poke = poke .. "\"special_attack\": " .. memory.read_u16_be(lvlAddr + 13) .. ", "
 poke = poke .. "\"special_defense\": " .. memory.read_u16_be(lvlAddr + 15) .. ", "
 poke = poke .. "\"is_shiny\": " .. getIsShiny(lvlAddr) .. ""

 return poke .. "}"
end

function buildEnemyPoke()
 poke = "\"enemy\": { "
 poke = poke .. "\"id\": \"" .. memory.readbyte(POKE_ENEMY_ID_ADDR) .. "\"" .. ", "
 poke = poke .. "\"level\": " .. memory.readbyte(POKE_ENEMY_LEVEL_ADDR) .. ", "
 poke = poke .. "\"types\": [" .. getEnemyTypes() .. "], "
 poke = poke .. "\"is_shiny\": " .. getIsShiny(POKE_ENEMY_IV_ADDR) .. " "

 return poke .. "}"
end

memory.usememorydomain("ROM")
gameCode = memory.readbyte(GAME_ADDR)

if gameCode == SILVER then
    game = 'silver'
elseif gameCode == CRYSTAL then
    game = 'crystal'
    loadCrystalAddresses()
else
    game = 'gold'
end

print('pokemon ' .. game .. ' version tracker')

while true do
	if diff > timeLimit then
	    mail()
	    memory.usememorydomain("WRAM")
		output = "{ " .. "\"game\":\"" .. game .. "\", \"team\": {"
		diff = -1
		size = memory.readbyte(TEAM_SIZE_ADDR)
		if view ~= "team" then
		    if size > 1 then
		        size = 1
		    end
		end

		output = output .. "\"size\": " .. size .. ", "
		output = output .. "\"view\": \"" .. view .. "\", "
		output = output .. "\"has_starter\": " .. memory.readbyte(GOT_STARTER_ADDR) .. ", "
		output = output .. buildPoke(1, POKE_1_NAME_ADDR, POKE_1_ID_ADDR, POKE_1_LEVEL_ADDR) .. "}, "
        output = output .. "\"battleType\": \"" .. memory.readbyte(BATTLE_TYPE) .. "\", "
        output = output .. buildEnemyPoke()

		
		output = output .. "}"

		file = io.open("poke.json", "w+")
		io.output(file)
		io.write(output)
		io.close(file)
	end
	diff = diff + 1
	emu.frameadvance()
end
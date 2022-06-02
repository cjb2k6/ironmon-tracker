timeLimit = 60
diff = 0

game='red'

view='lead'

NAME_LENGTH = 10

TEAM_SIZE_ADDR = tonumber("0x1163")

POKE_ENEMY_ID_ADDR = tonumber("0x0FD8")
POKE_ENEMY_LEVEL_ADDR = tonumber("0x0FF3")
POKE_ENEMY_IV_ADDR = tonumber("0x0FF1")

POKE_1_NAME_ADDR = tonumber("0x12B5")
POKE_1_ID_ADDR = tonumber("0x1164")
POKE_1_HP_ADDR = tonumber("0x116C")
POKE_1_LEVEL_ADDR = tonumber("0x118C")
POKE_1_START_ADDR = tonumber("0x116B")

BATTLE_TYPE = tonumber("0x1057")

MOVE_OFFSET = 8
PP_OFFSET = 29

GAME_ADDR = tonumber("0x013C")
RED = 82
BLUE = 66
YELLOW = 89

function loadYellowAddresses()
    POKE_1_START_ADDR = POKE_1_START_ADDR - 1
    POKE_1_ID_ADDR = POKE_1_ID_ADDR - 1
    POKE_1_HP_ADDR = POKE_1_HP_ADDR - 1
    POKE_1_NAME_ADDR = POKE_1_NAME_ADDR - 1
    POKE_1_LEVEL_ADDR = tonumber("0x118B")
    BATTLE_TYPE = BATTLE_TYPE - 1
    POKE_ENEMY_ID_ADDR = POKE_ENEMY_ID_ADDR - 1
    POKE_ENEMY_LEVEL_ADDR = tonumber("0x0FF2")
    POKE_ENEMY_IV_ADDR = POKE_ENEMY_IV_ADDR - 1
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

function getMaxHPAddr(pokeNumber)
    if pokeNumber == 1 then
        return POKE_1_LEVEL_ADDR + 1
    end
    if pokeNumber == 2 then
        return POKE_2_LEVEL_ADDR + 1
    end
    if pokeNumber == 3 then
        return POKE_3_LEVEL_ADDR + 1
    end
    if pokeNumber == 4 then
        return POKE_4_LEVEL_ADDR + 1
    end
    if pokeNumber == 5 then
        return POKE_5_LEVEL_ADDR + 1
    end

    return POKE_6_LEVEL_ADDR + 1
end

function getHPAddr(pokeNumber)
    if pokeNumber == 1 then
        return POKE_1_HP_ADDR
    end
    if pokeNumber == 2 then
        return POKE_2_HP_ADDR
    end
    if pokeNumber == 3 then
        return POKE_3_HP_ADDR
    end
    if pokeNumber == 4 then
        return POKE_4_HP_ADDR
    end
    if pokeNumber == 5 then
        return POKE_5_HP_ADDR
    end

    return POKE_6_HP_ADDR
end

function buildPoke(number, nameAddr, idAddr, lvlAddr, startAddr)
 poke = "\"poke" .. number .. "\": {"
 poke = poke .. "\"name\": " .. getPokeName(nameAddr) .. ", "
 poke = poke .. "\"id\": \"" .. memory.readbyte(idAddr) .. "\"" .. ", "
 poke = poke .. "\"item\": \"" .. "0" .. "\"" .. ", "
  poke = poke .. "\"move_1\": \"" .. memory.readbyte(startAddr + MOVE_OFFSET) .. "\"" .. ", "
 poke = poke .. "\"move_2\": \"" .. memory.readbyte(startAddr + MOVE_OFFSET + 1) .. "\"" .. ", "
 poke = poke .. "\"move_3\": \"" .. memory.readbyte(startAddr  + MOVE_OFFSET + 2) .. "\"" .. ", "
 poke = poke .. "\"move_4\": \"" .. memory.readbyte(startAddr + MOVE_OFFSET + 3) .. "\"" .. ", "
 poke = poke .. "\"pp_1\": \"" .. getPP(memory.readbyte(startAddr + PP_OFFSET)) .. "\"" .. ", "
 poke = poke .. "\"pp_2\": \"" .. getPP(memory.readbyte(startAddr + PP_OFFSET + 1)) .. "\"" .. ", "
 poke = poke .. "\"pp_3\": \"" .. getPP(memory.readbyte(startAddr + PP_OFFSET + 2)) .. "\"" .. ", "
 poke = poke .. "\"pp_4\": \"" .. getPP(memory.readbyte(startAddr + PP_OFFSET + 3)) .. "\"" .. ", "
 poke = poke .. "\"level\": " .. memory.readbyte(lvlAddr) .. ", "
 poke = poke .. "\"hp\": " .. memory.read_u16_be(getHPAddr(number)) .. ", "
 poke = poke .. "\"max_hp\": " .. memory.read_u16_be(getMaxHPAddr(number)) .. ", "
 poke = poke .. "\"attack\": " .. memory.read_u16_be(getMaxHPAddr(number) + 2) .. ", "
 poke = poke .. "\"defense\": " .. memory.read_u16_be(getMaxHPAddr(number) + 4) .. ", "
 poke = poke .. "\"speed\": " .. memory.read_u16_be(getMaxHPAddr(number) + 6) .. ", "
 poke = poke .. "\"special_attack\": " .. memory.read_u16_be(getMaxHPAddr(number) + 8) .. ", "
 poke = poke .. "\"special_defense\": " .. memory.read_u16_be(getMaxHPAddr(number) + 8) .. ", "
 poke = poke .. "\"is_shiny\": " .. 0 .. ""

 return poke .. "}"
end

function buildEnemyPoke()
 poke = "\"enemy\": { "
 poke = poke .. "\"id\": \"" .. memory.readbyte(POKE_ENEMY_ID_ADDR) .. "\"" .. ", "
 poke = poke .. "\"level\": " .. memory.readbyte(POKE_ENEMY_LEVEL_ADDR) .. ", "
 poke = poke .. "\"is_shiny\": " .. 0 .. " "

 return poke .. "}"
end

memory.usememorydomain("ROM")
gameCode = memory.readbyte(GAME_ADDR)

if gameCode == BLUE then
    game = 'blue'
elseif gameCode == YELLOW then
    game = 'yellow'
    loadYellowAddresses()
else
    game = 'red'
end

print('pokemon ' .. game .. ' version tracker')

memory.usememorydomain("WRAM")
while true do
	if diff > timeLimit then
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
		output = output .. buildPoke(1, POKE_1_NAME_ADDR, POKE_1_ID_ADDR, POKE_1_LEVEL_ADDR, POKE_1_START_ADDR) .. "}, "
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
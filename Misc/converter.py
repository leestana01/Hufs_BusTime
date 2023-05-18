# [파일 설명]
# 버스 시간표를 DB에 적용하기 원활한 방식으로 변환해주는 코드입니다.
# BeforeConvert에 존재하는 값을 기준으로 변환하여 AfterConvert에 저장합니다 :)


with open("BeforeConvert.txt", "r", encoding='utf-8') as file:
    lines = file.readlines()

converted_data = {}
nowDay = ""

for line in lines:
    line = line.strip()

    if line.startswith("@"):
        nowDay = line
        converted_data[nowDay] = {}
    elif line.startswith("["):
        bus = line[2:-1]  # "#" 제거
        converted_data[nowDay][bus] = []
    elif line == "":
        continue
    else:
        converted_data[nowDay][bus].append(line)

with open("AfterConvert.txt", "w", encoding='utf-8') as file:
    for key, value in converted_data.items():
        file.write(f"{key}\n")
        for subkey, subvalue in value.items():
            # 리스트-> 문자열 변환
            listvalue = str(subvalue).replace('\'', '\"')
            file.write(f"{subkey}: {listvalue},\n")
        file.write("\n")

print("변환 완료!")

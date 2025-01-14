% in the name of ALLAH
% ReadCDB: Reads a .cdb file and stores them in two variables "Data" and "Lables"
% Developed by: Hossein Khosravi
% www.FarsiOCR.ir
% 2010-OCT-29

% clear all;
clc;
MAX_COMMENT  = 512; %Maximum Comment size in byte

ShowImages = true
SaveImages = false
filename = 'Persian-Character-DB-Training.cdb';

fid = fopen(filename, 'rb');

%read private header
header = fread(fid, 7, 'uint8');
yy = fread(fid, 1, 'uint16');
m = fread(fid, 1, 'uint8');
d = fread(fid, 1, 'uint8');
W = fread(fid, 1, 'uint16');
H = fread(fid, 1, 'uint16');
TotalRec = fread(fid, 1, 'uint32');
nMaxCount = fread(fid, 1, 'uint16');
LetterCount = fread(fid, nMaxCount, 'uint32');
imgType = fread(fid, 1, 'uint8');%0: binary, 1: gray
Comments = fread(fid, MAX_COMMENT, '*char');
fprintf('%s\n', Comments);
Reserved = fread(fid, 490, 'uint8');
if( (W > 0) && (H > 0))
    normal = true
else
    normal = false
end;

Data = cell(TotalRec,1);
labels = zeros(TotalRec,1);

for i = 1:TotalRec
    StartWORD = fread(fid, 1, 'uint16'); % Must be 0xFFFF
    labels(i) = fread(fid, 1, 'uint16'); % Correct lable of the character
    Confidence = fread(fid, 1, 'uint16'); % Not important
    if (~normal)
        W = fread(fid, 1, 'uint16');
        H = fread(fid, 1, 'uint16');
    end;
    ByteCount = fread(fid, 1, 'uint16');
    Data{i} = uint8(zeros(H, W));

    if(imgType == 0) %Binary
        for y = 1:H
            bWhite = true;
            counter = 0;
            while (counter < W)
                WBcount = fread(fid, 1);
                x = 1;
                while(x <= WBcount)
                    if(bWhite)
                        Data{i}(y, x+counter) = 255; %Background
                    else
                        Data{i}(y, x+counter) = 0; %ForeGround
                    end;%if
                    x = x+1;
                end;%while(x <= WBcount)
                bWhite = ~bWhite; %black white black white ...
                counter = counter + WBcount;
            end;%while (counter < W)
        end;%y
    else %GrayScale mode
        Data{i} = transpose(reshape(uint8(fread(fid, W*H)), W, H));
    end;%else
    if ShowImages
        imshow(Data{i});
        title(sprintf('%d (%d*%d)', labels(i), W, H));
        pause;     
    end
    if(SaveImages)
        imwrite((Data{i}), sprintf('c:\\1\\%d_%d.bmp',i,labels(i)));
    end        
end;%for loop (i)
fclose(fid);
function ret = F_CLAHE_simple(input,upbound)
    input_T = double(input);
    output  = zeros(size(input));
    [row,col,~] = size(input_T);
    
    for i = 1:row
        for j = 1:col
            pad_row1 = max(1,i-16);
            pad_row2 = min(row,i+16);
            pad_col1 = max(1,j-16);
            pad_col2 = min(col,j+16);
            tmp = input_T(pad_row1:pad_row2,pad_col1:pad_col2,:);
            CDF = CLHE_CDF(tmp,upbound);
            output(i,j,:) = CDF(input(i,j,:))*255;
        end
    end
    ret = uint8(output);
end
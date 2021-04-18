function ret = F_Fogtest(input,m,A,beta)
    I=double(input);
    [row,col,alpha] = size(I);
    output = zeros(row,col,alpha);
    for i=1:alpha
        for j=1:row
            for l=1:col
                d(j,l) = -0.05*abs(j-m) + 13;  
                td(j,l) = exp(-beta*d(j,l));   %离所选焦点越远，其雾化程度越小，因为td代表原图保留率
                output(j,l,i) = I(j,l,i)/255*td(j,l) + A *(1-td(j,l)); %增加一个常数补充亮度，使雾变成白色
            end
        end
    end
    ret = uint8(output*255);
end
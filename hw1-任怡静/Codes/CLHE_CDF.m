function CDF = CLHE_CDF(input,upbound)
    %对当前的输入，整体求出CDF
    input_T = double(input);
    %[raw,col,alpha] = size(input_T);
    PMF = histcounts(input_T,0:1:256);%直方图
    PMF = PMF/sum(PMF); %直方图改成概率密度图
    upbound = max(PMF)*upbound; %按比例取upbound，否则概率会偏小
    peak = sum(PMF(PMF>upbound)-upbound); %对超过upbound的部分积分
    PMF_cut = min(PMF,upbound);%把PMF超过upbound部分削峰
    PMF_new = PMF_cut + peak/length(PMF);
    CDF = zeros(size(PMF));
    for i = 1:length(CDF)
        CDF(i) = sum(PMF_new(1:i));
    end
    %output = CDF(input)*255;
end
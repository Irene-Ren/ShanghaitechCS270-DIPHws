function CDF = CLHE_CDF(input,upbound)
    %�Ե�ǰ�����룬�������CDF
    input_T = double(input);
    %[raw,col,alpha] = size(input_T);
    PMF = histcounts(input_T,0:1:256);%ֱ��ͼ
    PMF = PMF/sum(PMF); %ֱ��ͼ�ĳɸ����ܶ�ͼ
    upbound = max(PMF)*upbound; %������ȡupbound��������ʻ�ƫС
    peak = sum(PMF(PMF>upbound)-upbound); %�Գ���upbound�Ĳ��ֻ���
    PMF_cut = min(PMF,upbound);%��PMF����upbound��������
    PMF_new = PMF_cut + peak/length(PMF);
    CDF = zeros(size(PMF));
    for i = 1:length(CDF)
        CDF(i) = sum(PMF_new(1:i));
    end
    %output = CDF(input)*255;
end
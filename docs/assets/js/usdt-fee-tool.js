(function () {
  const dataNode = document.getElementById("usdt-fee-tool-data");
  if (!dataNode) return;

  let payload;
  try {
    payload = JSON.parse(dataNode.textContent);
  } catch (_error) {
    return;
  }

  const moneyFormatter = new Intl.NumberFormat("en-US", {
    style: "currency",
    currency: "USD",
    minimumFractionDigits: 2,
    maximumFractionDigits: 3
  });

  const integerFormatter = new Intl.NumberFormat("en-US", {
    minimumFractionDigits: 0,
    maximumFractionDigits: 0
  });

  const decimalFormatter = new Intl.NumberFormat("en-US", {
    minimumFractionDigits: 0,
    maximumFractionDigits: 3
  });

  function formatMoney(value) {
    if (value === 0) return "$0";
    if (value < 0.01) return "$" + value.toFixed(3);
    return moneyFormatter.format(value);
  }

  function formatPercent(fee, amount) {
    if (fee === 0) return "0%";
    const ratio = (fee / amount) * 100;
    if (ratio < 0.01) return ratio.toFixed(3) + "%";
    if (ratio < 1) return ratio.toFixed(2) + "%";
    return ratio.toFixed(1) + "%";
  }

  function formatNumber(value) {
    return integerFormatter.format(value);
  }

  function formatDecimal(value) {
    return decimalFormatter.format(value);
  }

  function formatAmountLabel(amount) {
    return formatNumber(amount) + " USDT";
  }

  function clampPositiveNumber(raw, fallback) {
    const value = Number(raw);
    if (!Number.isFinite(value) || value <= 0) return fallback;
    return value;
  }

  function renderFeeTool() {
    const tool = document.querySelector("[data-fee-tool]");
    if (!tool) return;

    const amountInput = tool.querySelector("[data-amount-input]");
    const profileSelect = tool.querySelector("[data-profile-select]");
    const tableBody = tool.querySelector("[data-fee-table-body]");
    const presetButtons = tool.querySelectorAll("[data-amount-preset]");

    function rankRows(amount, profile) {
      return payload.networks
        .map((network) => ({
          ...network,
          fee: network.feeUsd[profile]
        }))
        .sort((a, b) => a.fee - b.fee);
    }

    function renderTable(rows, amount) {
      tableBody.innerHTML = rows
        .map(
          (network, index) => `
            <tr>
              <td>#${index + 1}</td>
              <td>
                <strong>${network.name}</strong>
                <div class="fee-table-sub">${network.family}</div>
              </td>
              <td>${formatMoney(network.fee)}</td>
              <td>${formatPercent(network.fee, amount)}</td>
              <td>${network.speed}</td>
              <td>${network.gasToken}</td>
              <td>${network.bestFor}</td>
              <td>${network.watchFor}</td>
            </tr>
          `
        )
        .join("");
    }

    function render() {
      const amount = clampPositiveNumber(amountInput.value, 1000);
      const profile = profileSelect.value;
      const profileMeta =
        payload.profiles.find((item) => item.id === profile) || payload.profiles[1];
      const rows = rankRows(amount, profileMeta.id);

      amountInput.value = amount;
      renderTable(rows, amount);
    }

    amountInput.addEventListener("input", render);
    profileSelect.addEventListener("change", render);
    presetButtons.forEach((button) => {
      button.addEventListener("click", function () {
        amountInput.value = button.getAttribute("data-amount-preset");
        render();
      });
    });

    render();
  }

  function renderEnergyTool() {
    const tool = document.querySelector("[data-energy-tool]");
    if (!tool) return;

    const stakedInput = tool.querySelector("[data-staked-trx]");
    const countInput = tool.querySelector("[data-transfer-count]");
    const addressTypeSelect = tool.querySelector("[data-address-type]");
    const modeSelect = tool.querySelector("[data-energy-mode]");
    const summary = tool.querySelector("[data-energy-summary]");
    const note = tool.querySelector("[data-energy-note]");
    const table = tool.querySelector("[data-energy-table]");
    const presetButtons = tool.querySelectorAll("[data-stake-preset]");
    const tron = payload.tronEnergy;

    function render() {
      const stakedTrx = Math.max(0, Number(stakedInput.value) || 0);
      const transferCount = clampPositiveNumber(countInput.value, 1);
      const addressType = addressTypeSelect.value === "new" ? "new" : "old";
      const transferEnergy =
        addressType === "new"
          ? tron.transferEnergy.newAddress
          : tron.transferEnergy.oldAddress;
      const mode = tron.modes[modeSelect.value] || tron.modes.current;
      const estimatedDailyEnergy = Math.floor(stakedTrx * mode.energyPerTrx);
      const requiredEnergy = transferCount * transferEnergy;
      const coveredTransfers = Math.floor(estimatedDailyEnergy / transferEnergy);
      const gapEnergy = Math.max(0, requiredEnergy - estimatedDailyEnergy);
      const extraStake = gapEnergy === 0 ? 0 : Math.ceil(gapEnergy / mode.energyPerTrx);
      const minimumStakeOneTransfer = Math.ceil(transferEnergy / mode.energyPerTrx);
      const enough = gapEnergy === 0;
      const burnTrxEquivalent = requiredEnergy / 10000;

      stakedInput.value = stakedTrx;
      countInput.value = transferCount;

      note.textContent =
        `${mode.label}：${mode.description}。当前按 1 TRX ≈ ${formatDecimal(mode.energyPerTrx)} Energy / 天估算；${addressType === "new" ? "新地址" : "已持有过 USDT 的地址"}按 ${formatNumber(transferEnergy)} Energy / 笔计算。`;

      summary.innerHTML = [
        {
          kicker: "预计可得能量",
          title: formatNumber(estimatedDailyEnergy),
          note: `按 ${formatDecimal(mode.energyPerTrx)} Energy / TRX / 天计算`
        },
        {
          kicker: "大概能覆盖",
          title: `${formatNumber(coveredTransfers)} 笔`,
          note: `${addressType === "new" ? "新地址" : "老地址"}口径：${formatNumber(transferEnergy)} Energy / 笔`
        },
        {
          kicker: "当前判断",
          title: enough ? "够转" : "还不够",
          note: enough
            ? `覆盖 ${formatNumber(transferCount)} 笔需求`
            : `还差 ${formatNumber(gapEnergy)} Energy`
        }
      ]
        .map(
          (item) => `
            <div class="fee-summary-card">
              <span class="card-kicker">${item.kicker}</span>
              <strong>${item.title}</strong>
              <p>${item.note}</p>
            </div>
          `
        )
        .join("");

      table.innerHTML = `
        <tr><th>你现在质押的 TRX</th><td>${formatNumber(stakedTrx)} TRX</td></tr>
        <tr><th>预计每日可得能量</th><td>${formatNumber(estimatedDailyEnergy)} Energy</td></tr>
        <tr><th>计划转账笔数</th><td>${formatNumber(transferCount)} 笔</td></tr>
        <tr><th>当前按每笔多少能量算</th><td>${formatNumber(transferEnergy)} Energy / 笔</td></tr>
        <tr><th>这次总共需要多少能量</th><td>${formatNumber(requiredEnergy)} Energy</td></tr>
        <tr><th>够不够覆盖</th><td>${enough ? "够。覆盖内可视为 $0 额外链上成本" : "不够。需要额外补质押、租能量，或让钱包直烧 TRX"}</td></tr>
        <tr><th>还差多少能量</th><td>${formatNumber(gapEnergy)} Energy</td></tr>
        <tr><th>按当前模式还要多质押多少 TRX</th><td>${formatNumber(extraStake)} TRX</td></tr>
        <tr><th>如果只想覆盖 1 笔，理论起步值</th><td>${formatNumber(minimumStakeOneTransfer)} TRX</td></tr>
        <tr><th>如果完全不质押，等价要烧多少 TRX</th><td>约 ${formatDecimal(burnTrxEquivalent)} TRX（按 1 TRX ≈ 10,000 Energy 粗算）</td></tr>
        <tr><th>TRXDeFi 下单时你真正要填什么</th><td><code>payNums = ${formatNumber(requiredEnergy)}</code>，也就是你要租的 Energy 数量，不是“几笔”</td></tr>
      `;
    }

    [stakedInput, countInput].forEach((input) => {
      input.addEventListener("input", render);
    });
    [addressTypeSelect, modeSelect].forEach((select) => {
      select.addEventListener("change", render);
    });
    presetButtons.forEach((button) => {
      button.addEventListener("click", function () {
        stakedInput.value = button.getAttribute("data-stake-preset");
        render();
      });
    });

    render();
  }

  renderFeeTool();
  renderEnergyTool();
})();

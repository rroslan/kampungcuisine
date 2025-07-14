// Cart Management JavaScript
// Handles cart updates, messaging, and UI interactions

document.addEventListener("DOMContentLoaded", function () {
  // Initialize cart functionality
  initializeCart();
});

function initializeCart() {
  // Handle HTMX responses for cart updates
  document.body.addEventListener("htmx:afterRequest", function (event) {
    handleCartResponse(event);
  });

  // Handle regular form submissions that return JSON
  document.body.addEventListener("htmx:responseError", function (event) {
    showCartMessage("Something went wrong", "error");
  });

  // Update cart count on page load
  updateCartCountFromServer();
}

function handleCartResponse(event) {
  // Check if the response is JSON
  const contentType = event.detail.xhr.getResponseHeader("content-type");

  if (contentType && contentType.includes("application/json")) {
    try {
      const response = JSON.parse(event.detail.xhr.responseText);

      if (response.success) {
        // Show success message
        if (response.message) {
          showCartMessage(response.message, "success");
        }

        // Update cart count in navigation
        if (typeof response.cart_count !== "undefined") {
          updateCartCount(response.cart_count);
        }

        // Update cart total in navigation
        if (typeof response.cart_total !== "undefined") {
          updateCartTotal(response.cart_total);
        }

        // Handle item removal
        if (response.item_removed) {
          // Refresh cart items if we're on the cart page
          refreshCartIfOnCartPage();
        }
      } else {
        showCartMessage(response.message || "Error", "error");
      }
    } catch (e) {
      // Not JSON response or parsing error, ignore
      console.log("Non-JSON response or parsing error:", e);
    }
  }
}

function updateCartCount(count) {
  // Update all cart count elements
  const cartCountElements = document.querySelectorAll("[data-cart-count]");
  cartCountElements.forEach((element) => {
    element.textContent = count;

    // Show/hide based on count
    if (count > 0) {
      element.style.display = "inline";
      // Update Alpine.js data if available
      if (element.closest("[x-data]") && element.closest("[x-data]").__x) {
        element.closest("[x-data]").__x.$data.cartCount = count;
      }
    } else {
      element.style.display = "none";
      // Update Alpine.js data if available
      if (element.closest("[x-data]") && element.closest("[x-data]").__x) {
        element.closest("[x-data]").__x.$data.cartCount = 0;
      }
    }
  });
}

function updateCartTotal(total) {
  // Update cart total in navigation dropdown
  const cartTotalElements = document.querySelectorAll("[data-cart-total]");
  cartTotalElements.forEach((element) => {
    element.textContent = `$${parseFloat(total).toFixed(2)}`;
  });
}

function showCartMessage(message, type = "success") {
  // Create or get message container
  let messageContainer = document.getElementById("cart-messages");

  if (!messageContainer) {
    messageContainer = document.createElement("div");
    messageContainer.id = "cart-messages";
    messageContainer.className = "fixed top-4 right-4 z-50 space-y-2";
    document.body.appendChild(messageContainer);
  }

  // Create message element
  const alertClass = type === "success" ? "alert-success" : "alert-error";
  const iconPath =
    type === "success"
      ? "M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"
      : "M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z";

  const bgClass = type === "success" ? "alert-success" : "alert-warning";

  const messageElement = document.createElement("div");
  messageElement.className = `alert ${bgClass} shadow-xl max-w-sm animate-in slide-in-from-right duration-300`;
  messageElement.innerHTML = `
        <div class="flex items-center">
            <svg class="w-5 h-5 mr-3 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="${iconPath}"></path>
            </svg>
            <span class="font-medium text-sm">${message}</span>
            <button onclick="this.closest('.alert').remove()" class="ml-auto btn btn-sm btn-ghost btn-circle" title="Dismiss">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
                </svg>
            </button>
        </div>
    `;

  messageContainer.appendChild(messageElement);

  // Auto-remove message after 4 seconds with fade out
  setTimeout(() => {
    if (messageElement.parentNode) {
      messageElement.style.transition = "opacity 0.3s ease-out";
      messageElement.style.opacity = "0";
      setTimeout(() => {
        if (messageElement.parentNode) {
          messageElement.remove();
        }
      }, 300);
    }
  }, 4000);
}

function updateCartCountFromServer() {
  // Fetch current cart count from server
  fetch("/cart/count/")
    .then((response) => response.json())
    .then((data) => {
      updateCartCount(data.cart_count);
      updateCartTotal(data.cart_total);
    })
    .catch((error) => {
      console.error("Cart count update failed:", error);
    });
}

function refreshCartIfOnCartPage() {
  // Check if we're on the cart page and refresh if needed
  if (window.location.pathname.includes("/cart/")) {
    // Use HTMX to refresh cart items
    const cartItemsContainer = document.getElementById("cart-items");
    if (cartItemsContainer) {
      htmx.ajax("GET", "/cart/partials/items/", {
        target: "#cart-items",
        swap: "outerHTML",
      });
    }

    const cartSummaryContainer = document.getElementById("cart-summary");
    if (cartSummaryContainer) {
      htmx.ajax("GET", "/cart/partials/summary/", {
        target: "#cart-summary",
        swap: "outerHTML",
      });
    }
  }
}

// Utility functions for quantity controls
function increaseQuantity(inputId) {
  const input = document.getElementById(inputId);
  if (input) {
    const currentValue = parseInt(input.value) || 1;
    if (currentValue < 99) {
      input.value = currentValue + 1;
    }
  }
}

function decreaseQuantity(inputId) {
  const input = document.getElementById(inputId);
  if (input) {
    const currentValue = parseInt(input.value) || 1;
    if (currentValue > 1) {
      input.value = currentValue - 1;
    }
  }
}

// Quick add to cart function for product grids
function quickAddToCart(productId, quantity = 1) {
  const form = document.createElement("form");
  form.style.display = "none";

  const csrfToken = document.querySelector("[name=csrfmiddlewaretoken]");
  if (csrfToken) {
    const csrfInput = document.createElement("input");
    csrfInput.type = "hidden";
    csrfInput.name = "csrfmiddlewaretoken";
    csrfInput.value = csrfToken.value;
    form.appendChild(csrfInput);
  }

  const quantityInput = document.createElement("input");
  quantityInput.type = "hidden";
  quantityInput.name = "quantity";
  quantityInput.value = quantity;
  form.appendChild(quantityInput);

  document.body.appendChild(form);

  // Use HTMX to submit
  htmx
    .ajax("POST", `/cart/add/${productId}/`, {
      source: form,
      swap: "none",
    })
    .then(() => {
      document.body.removeChild(form);
    });
}

// Handle cart icon animation
function animateCartIcon() {
  const cartIcons = document.querySelectorAll(".cart-icon");
  cartIcons.forEach((icon) => {
    icon.classList.add("animate-bounce");
    setTimeout(() => {
      icon.classList.remove("animate-bounce");
    }, 600);
  });
}

// Export functions for global use
window.cartUtils = {
  increaseQuantity,
  decreaseQuantity,
  quickAddToCart,
  updateCartCount,
  updateCartTotal,
  showCartMessage,
  animateCartIcon,
};

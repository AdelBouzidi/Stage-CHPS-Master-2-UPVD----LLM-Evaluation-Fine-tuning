program rescale_demo
  implicit none
  integer, parameter :: dp = kind(1.0d0)
  integer :: n
  real(dp), allocatable :: numbers(:)
  real(dp), allocatable :: rescaled(:)
  integer :: i

  ! Read input
  read(*,*) n
  allocate(numbers(n))
  read(*,*) numbers

  ! Call the rescale function
  call rescale_to_unit(n, numbers, rescaled)

  ! Output result
  print *, rescaled

contains

  subroutine rescale_to_unit(n, numbers, rescaled)
    implicit none
    integer, intent(in) :: n
    real(dp), intent(in) :: numbers(n)
    real(dp), intent(out) :: rescaled(n)
    real(dp) :: min_val, max_val, range

    min_val = numbers(1)
    do i = 2, n
      if (numbers(i) < min_val) min_val = numbers(i)
    end do

    max_val = numbers(1)
    do i = 2, n
      if (numbers(i) > max_val) max_val = numbers(i)
    end do

    range = max_val - min_val
    if (range == 0.0_dp) then
      rescaled = 0.0_dp
    else
      rescaled = (numbers - min_val) / range
    end if
  end subroutine rescale_to_unit

end program rescale_demo
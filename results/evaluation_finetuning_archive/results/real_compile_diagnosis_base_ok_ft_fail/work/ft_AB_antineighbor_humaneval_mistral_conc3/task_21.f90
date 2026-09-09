program rescale_demo
  implicit none
  integer, parameter :: dp = kind(1.0d0)
  integer :: numbers_len
  real(dp), allocatable :: numbers(:)
  real(dp), allocatable :: rescaled(:)
  integer :: i

  ! Read input
  read(*,*) numbers_len
  allocate(numbers(numbers_len))
  do i = 1, numbers_len
    read(*,*) numbers(i)
  end do

  ! Call the rescale function
  call rescale_to_unit(numbers_len, numbers, rescaled)

  ! Output results
  print *, 'Rescaled values:'
  do i = 1, numbers_len
    print *, rescaled(i)
  end do

contains

  subroutine rescale_to_unit(numbers_len, numbers, rescaled)
    implicit none
    integer, intent(in) :: numbers_len
    real(dp), intent(in) :: numbers(numbers_len)
    real(dp), intent(out) :: rescaled(numbers_len)
    real(dp) :: min_val, max_val, range

    min_val = numbers(1)
    max_val = numbers(1)
    do i = 2, numbers_len
      if (numbers(i) < min_val) min_val = numbers(i)
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
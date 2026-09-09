program even_odd_count_demo
  implicit none
  integer :: num
  integer :: even_count, odd_count
  character(len=1) :: digit

  ! Read input number
  read(*,*) num

  ! Initialize counters
  even_count = 0
  odd_count = 0

  ! Convert number to string and count digits
  write(num_str, '(I0)') abs(num)
  do i = 1, len(num_str)
    digit = num_str(i:i)
    if (iand(iachar(digit), 1) == 0) then
      even_count = even_count + 1
    else
      odd_count = odd_count + 1
    end if
  end do

  ! Output results
  print *, even_count, odd_count

contains

  function iand(a, b) result(res)
    integer, intent(in) :: a, b
    integer :: res
    res = iand(a, b)
  end function iand

  function iachar(c) result(res)
    character(len=*), intent(in) :: c
    integer :: res
    res = iachar(c(1:1))
  end function iachar

end program even_odd_count_demo